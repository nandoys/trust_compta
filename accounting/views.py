import datetime
import pandas as pd
import numpy as np
import json

from django.shortcuts import render, redirect, resolve_url
from django.contrib import messages
from django.db.models import Sum
from django.db.models.query import F, Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import RequestAborted, ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django.db.utils import IntegrityError, DataError
from django.utils.datastructures import MultiValueDictKeyError

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAcceptable, ValidationError
from rest_framework import status

from utils.files import upload_file, fs
from utils.calendar import months_of_year
from utils.treasury import outcomes_with_subaccount
from settings.models import Journal

from .models import Main, Additional, FiscalYear, Budget, Plan, PlanCategory
from .forms import MainAccountingForm, AdditionalAccountingForm, BudgetAccountingForm
from .serializer import MainSerializer, AdditionalSerializer, PlanSerializer

from treasury.models import Currency, Income, Outcome

# Create your views here.


currencies = list()

for curr in Currency.objects.all():
    currencies.append({
        'name': curr.name,
        'symbol': curr.symbol,
        'country_code': curr.country_code,
        'flag': 'images/flags/' + curr.country_code + '.svg'
    })


@login_required()
def index(request):
    year_id = request.session.get('year')
    try:
        fiscal_year = FiscalYear.objects.get(id=year_id)
    except FiscalYear.DoesNotExist:
        return redirect('account_logout')

    currency_cdf = Currency.objects.get(symbol='cdf')
    currency_usd = Currency.objects.get(symbol='usd')

    incomes_general_cdf = Income.objects.filter(currency=currency_cdf).all()
    incomes_general_usd = Income.objects.filter(currency=currency_usd).all()

    incomes_cdf = Income.objects.filter(currency=currency_cdf, in_at__year=fiscal_year.year).all()
    incomes_usd = Income.objects.filter(currency=currency_usd, in_at__year=fiscal_year.year).all()

    outcomes_general_cdf = Outcome.objects.filter(currency=currency_cdf).all()
    outcomes_general_usd = Outcome.objects.filter(currency=currency_usd).all()

    outcomes_cdf = Outcome.objects.filter(currency=currency_cdf, out_at__year=fiscal_year.year).all()
    outcomes_usd = Outcome.objects.filter(currency=currency_usd, out_at__year=fiscal_year.year).all()

    checkout_general_income_cdf = incomes_general_cdf.aggregate(Sum('amount'))
    balance_general_income_cdf = 0

    checkout_general_income_usd = incomes_general_usd.aggregate(Sum('amount'))
    balance_general_income_usd = 0

    total_checkout_income_cdf = incomes_cdf.aggregate(Sum('amount'))
    balance_income_cdf = 0

    total_checkout_income_usd = incomes_usd.aggregate(Sum('amount'))
    balance_income_usd = 0

    checkout_general_outcome_cdf = outcomes_general_cdf.aggregate(Sum('amount'))
    balance_general_outcome_cdf = 0

    checkout_general_outcome_usd = outcomes_general_usd.aggregate(Sum('amount'))
    balance_general_outcome_usd = 0

    total_checkout_outcome_cdf = outcomes_cdf.aggregate(Sum('amount'))
    balance_outcome_cdf = 0

    total_checkout_outcome_usd = outcomes_usd.aggregate(Sum('amount'))
    balance_outcome_usd = 0

    if checkout_general_income_cdf['amount__sum'] is not None:
        balance_general_income_cdf = checkout_general_income_cdf['amount__sum']

    if checkout_general_income_usd['amount__sum'] is not None:
        balance_general_income_usd = checkout_general_income_usd['amount__sum']

    if total_checkout_income_cdf['amount__sum'] is not None:
        balance_income_cdf = total_checkout_income_cdf['amount__sum']

    if total_checkout_income_usd['amount__sum'] is not None:
        balance_income_usd = total_checkout_income_usd['amount__sum']

    if checkout_general_outcome_cdf['amount__sum'] is not None:
        balance_general_outcome_cdf = checkout_general_outcome_cdf['amount__sum']

    if checkout_general_outcome_usd['amount__sum'] is not None:
        balance_general_outcome_usd = checkout_general_outcome_usd['amount__sum']

    if total_checkout_outcome_cdf['amount__sum'] is not None:
        balance_outcome_cdf = total_checkout_outcome_cdf['amount__sum']

    if total_checkout_outcome_usd['amount__sum'] is not None:
        balance_outcome_usd = total_checkout_outcome_usd['amount__sum']

    balance_cdf = balance_income_cdf - balance_outcome_cdf
    balance_usd = balance_income_usd - balance_outcome_usd

    balance_general_cdf = balance_general_income_cdf - balance_general_outcome_cdf
    balance_general_usd = balance_general_income_usd - balance_general_outcome_usd

    context = {
        'months': months_of_year(),
        'income': {
            'cdf': balance_income_cdf, 'usd': balance_income_usd
        },
        'outcome': {
            'cdf': balance_outcome_cdf, 'usd': balance_outcome_usd
        },
        'balance': {
            'cdf': balance_cdf, 'usd': balance_usd
        },
        'balance_general_cdf': balance_general_cdf,
        'balance_general_usd': balance_general_usd,
        'current_year': fiscal_year.year.__str__()
    }
    return render(request, 'accounting_plan/dashboard.html', context)


@login_required()
def overall(request, symbol):
    year_id = request.session.get('year')

    selected_month = request.GET.get('mois', 0)

    reporting_period = 'Annuel'

    for month in months_of_year():
        if selected_month != 0:
            if str(month['id']) == selected_month:
                reporting_period = month['name']
                break

    try:
        fiscal_year = FiscalYear.objects.get(id=year_id)
        currency = Currency.objects.get(symbol=symbol)
    except FiscalYear.DoesNotExist:
        return redirect('account_logout')
    except Currency.DoesNotExist:
        return redirect('accounting_index')

    main_acc_outcomes = Main.objects.filter(account_type='decaissement').all()

    main_acc_incomes = Main.objects.filter(account_type='encaissement').all()

    main_outcomes_reports = list()

    main_incomes_reports = list()

    total_general_incomes = 0
    total_general_outcomes = 0

    for main_acc_outcome in main_acc_outcomes:
        if selected_month == 0:
            total_outcomes = main_acc_outcome.outcome_set.filter(currency=currency, out_at__year=fiscal_year.year).all()
        else:
            total_outcomes = main_acc_outcome.outcome_set.filter(currency=currency, out_at__month=selected_month,
                                                                 out_at__year=fiscal_year.year).all()
        report_outcomes = total_outcomes.aggregate(Sum('amount'))
        balance_main_report = 0

        additional_acc_outcomes = main_acc_outcome.additional_set.all()

        additional_reports = list()
        for additional_acc_outcome in additional_acc_outcomes:
            if selected_month == 0:
                total_additional_acc_outcomes = additional_acc_outcome.outcome_set.filter(currency=currency,
                                                                                          out_at__year=fiscal_year.year).all()
            else:
                total_additional_acc_outcomes = additional_acc_outcome.outcome_set.filter(currency=currency,
                                                                                          out_at__month=selected_month,
                                                                                          out_at__year=fiscal_year.year).all()

            report_additional_acc_outcomes = total_additional_acc_outcomes.aggregate(Sum('amount'))
            balance_additional_report = 0

            adjunct_acc_outcomes = additional_acc_outcome.adjunct_set.all()

            adjunct_reports = list()
            for adjunct_acc_outcome in adjunct_acc_outcomes:
                if selected_month == 0:
                    total_adjunct_acc_outcomes = adjunct_acc_outcome.outcome_set.filter(currency=currency,
                                                                                        out_at__year=fiscal_year.year).all()
                else:
                    total_adjunct_acc_outcomes = adjunct_acc_outcome.outcome_set.filter(currency=currency,
                                                                                        out_at__month=selected_month,
                                                                                        out_at__year=fiscal_year.year).all()

                report_adjunct_acc_outcomes = total_adjunct_acc_outcomes.aggregate(Sum('amount'))
                balance_adjunct_report = 0

                if report_adjunct_acc_outcomes['amount__sum'] is not None:
                    balance_adjunct_report = report_adjunct_acc_outcomes['amount__sum']

                adjunct_reports.append({
                    'acc_name': adjunct_acc_outcome.adjunct_account_name,
                    'balance': balance_adjunct_report,
                    'currency': currency.symbol
                })

            if report_additional_acc_outcomes['amount__sum'] is not None:
                balance_additional_report = report_additional_acc_outcomes['amount__sum']

            additional_reports.append({
                'acc_name': additional_acc_outcome.account_name,
                'acc_number': additional_acc_outcome.account_number,
                'balance': balance_additional_report,
                'currency': currency.symbol,
                'acc_adjunct': adjunct_reports
            })

        if report_outcomes['amount__sum'] is not None:
            balance_main_report = report_outcomes['amount__sum']
            total_general_outcomes += balance_main_report

        main_outcomes_reports.append({
            'acc_name': main_acc_outcome.account_name,
            'acc_number': main_acc_outcome.account_number,
            'balance': balance_main_report,
            'currency': currency.symbol,
            'acc_additionals': additional_reports
        })

    for main_acc_income in main_acc_incomes:
        if selected_month == 0:
            total_incomes = main_acc_income.income_set.filter(currency=currency, in_at__year=fiscal_year.year).all()
        else:
            total_incomes = main_acc_income.income_set.filter(currency=currency, in_at__month=selected_month,
                                                              in_at__year=fiscal_year.year).all()
        report_incomes = total_incomes.aggregate(Sum('amount'))
        balance_main_report = 0

        additional_acc_incomes = main_acc_income.additional_set.all()

        additional_reports = list()
        for additional_acc_income in additional_acc_incomes:
            if selected_month == 0:
                total_additional_acc_incomes = additional_acc_income.income_set.filter(currency=currency,
                                                                                       in_at__year=fiscal_year.year).all()
            else:
                total_additional_acc_incomes = additional_acc_income.income_set.filter(currency=currency,
                                                                                       in_at__month=selected_month,
                                                                                       in_at__year=fiscal_year.year).all()

            report_additional_acc_incomes = total_additional_acc_incomes.aggregate(Sum('amount'))
            balance_additional_report = 0

            adjunct_acc_incomes = additional_acc_income.adjunct_set.all()

            adjunct_reports = list()
            for adjunct_acc_income in adjunct_acc_incomes:
                if selected_month == 0:
                    total_adjunct_acc_incomes = adjunct_acc_income.income_set.filter(currency=currency,
                                                                                     in_at__year=fiscal_year.year).all()
                else:
                    total_adjunct_acc_incomes = adjunct_acc_income.income_set.filter(currency=currency,
                                                                                     in_at__month=selected_month,
                                                                                     in_at__year=fiscal_year.year).all()

                report_adjunct_acc_incomes = total_adjunct_acc_incomes.aggregate(Sum('amount'))
                balance_adjunct_report = 0

                if report_adjunct_acc_incomes['amount__sum'] is not None:
                    balance_adjunct_report = report_adjunct_acc_incomes['amount__sum']

                adjunct_reports.append({
                    'acc_name': adjunct_acc_income.adjunct_account_name,
                    'balance': balance_adjunct_report,
                    'currency': currency.symbol
                })

            if report_additional_acc_incomes['amount__sum'] is not None:
                balance_additional_report = report_additional_acc_incomes['amount__sum']

            additional_reports.append({
                'acc_name': additional_acc_income.account_name,
                'acc_number': additional_acc_income.account_number,
                'balance': balance_additional_report,
                'currency': currency.symbol,
                'acc_adjunct': adjunct_reports
            })

        if report_incomes['amount__sum'] is not None:
            balance_main_report = report_incomes['amount__sum']
            total_general_incomes += balance_main_report

        main_incomes_reports.append({
            'acc_name': main_acc_income.account_name,
            'acc_number': main_acc_income.account_number,
            'balance': balance_main_report,
            'currency': currency.symbol,
            'acc_additionals': additional_reports
        })
    context = {
        'income_reports': main_incomes_reports,
        'outcome_reports': main_outcomes_reports,
        'total_general_incomes': total_general_incomes,
        'total_general_outcomes': total_general_outcomes,
        'url': '/comptabilite',
        'currency': currency.symbol.upper(),
        'reporting_period': reporting_period,
        'reporting_title': 'Reporting {}'.format(reporting_period),
        'months': months_of_year(),
        'current_year': str(fiscal_year.year)
    }
    return render(request, 'accounting_plan/overall.html', context)


@login_required()
def accounting_plan(request):
    year_id = request.session.get('year')
    get_month = request.session.get('mois', 1)

    try:
        fiscal_year = FiscalYear.objects.get(id=year_id)
    except FiscalYear.DoesNotExist:
        return redirect('account_logout')

    selected_month = dict()
    for m in months_of_year():
        if m.get('id') == get_month:
            selected_month = m

    currency = Currency.objects.get(symbol='usd')

    if request.method == 'POST':

        if request.FILES.get('fileplan'):
            file = request.FILES['filebudget']

            def save_budget(account, row):
                for i in range(1, 13):
                    amount = row[i + 1]
                    plan_at = datetime.date.replace(datetime.date.today(), fiscal_year.year, i, 1)
                    budget = Budget(accounting=account, plan_at=plan_at, amount=amount)
                    budget.save()

            if file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                path = upload_file(file)

                df = pd.read_excel(path)

            elif file.content_type == 'text/csv':
                path = upload_file(file)
                df = pd.read_csv(path, sep=";")
                for row in df.values:
                    account_number = row[0]

                    try:
                        additional_account = Additional.objects.get(account_number=account_number)
                        save_budget(additional_account, row)
                    except Additional.DoesNotExist:
                        raise ObjectDoesNotExist("Ce compte n'existe pas")

            else:
                raise RequestAborted()

        if 'delete-item' in request.POST.keys():
            main_accounting = Main.objects.filter(id=request.POST['delete-item'])
            main_accounting.delete()
        else:
            if len(request.POST['update-item']) > 0:
                pk = request.POST['update-item']
                main_account = Main.objects.get(id=pk)
                accounting_form = MainAccountingForm(request.POST, instance=main_account)
                accounting_form.save()

            accounting_form = MainAccountingForm(request.POST)
            if accounting_form.is_valid():
                accounting_form.save()
                messages.success(request, 'Compte ajouté avec succès')
            else:
                messages.error(request, 'Les valeurs envoyées sont incorrectes')

        return redirect('accounting_plan')

    main_accountings = Main.objects.all()

    overalls = list()

    for accounting in main_accountings:

        if accounting.account_type == 'encaissement':
            try:
                incomes = Income.objects.filter(in_at__year=fiscal_year.year, accounting_main=accounting)
                total_incomes = incomes.aggregate(Sum('amount'))['amount__sum']
                overalls.append({
                    'id': accounting.id,
                    'account_number': accounting.account_number,
                    'account_name': accounting.account_name,
                    'account_type': accounting.account_type,
                    'total': total_incomes
                })
            except Income.DoesNotExist:
                overalls.append({
                    'id': accounting.id,
                    'account_number': accounting.account_number,
                    'account_name': accounting.account_name,
                    'account_type': accounting.account_type,
                    'total': 0
                })
        else:
            try:
                outcomes = Outcome.objects.filter(out_at__year=fiscal_year.year, accounting_main=accounting)
                total_outcomes = outcomes.aggregate(Sum('amount'))['amount__sum']
                overalls.append({
                    'id': accounting.id,
                    'account_number': accounting.account_number,
                    'account_name': accounting.account_name,
                    'account_type': accounting.account_type,
                    'total': total_outcomes
                })
            except Outcome.DoesNotExist:
                overalls.append({
                    'id': accounting.id,
                    'account_number': accounting.account_number,
                    'account_name': accounting.account_name,
                    'account_type': accounting.account_type,
                    'total': 0
                })

    form = MainAccountingForm()
    context = {
        'main_accountings': main_accountings,
        'overalls': overalls,
        'form': form,
        'fiscal_year': fiscal_year,
        'selected_month': selected_month,
        'currencies': currencies,
        'currency': currency,
        'url': '/comptabilite',
        'current_checkout': 'images/flags/' + currency.country_code + '.svg',
    }
    return render(request, 'accounting_plan/plan.html', context)


@login_required()
def accounting_main_details(request, pk):
    try:
        main_accounting = Main.objects.filter(id=pk).get()
        additional_accountings = Additional.objects.filter(account_main=pk).all()

        if request.method == 'POST':

            if 'delete-item' in request.POST.keys():

                additional_accounting = Additional.objects.filter(id=request.POST['delete-item'])
                additional_accounting.delete()
            else:
                if len(request.POST['update-item']) > 0:
                    pk = request.POST['update-item']
                    additional_account = Additional.objects.get(id=pk)
                    accounting_form = AdditionalAccountingForm(request.POST, instance=additional_account)
                    accounting_form.save()

                accounting_form = AdditionalAccountingForm(request.POST)

                account_number = accounting_form['account_number'].value()
                account_name = accounting_form['account_name'].value()

                if accounting_form.is_valid():
                    instance = accounting_form.save(commit=False)
                    instance.account_main = main_accounting
                    instance.save()

                    has_account = Additional.objects.filter(
                        Q(account_number=account_number) | Q(account_name=account_name))
                    if not has_account.exists():
                        messages.success(request, 'Compte ajouté avec succès')
                else:

                    has_account = Additional.objects.filter(
                        Q(account_number=account_number) | Q(account_name=account_name))
                    if has_account.exists():
                        if has_account.get().account_number == account_number:
                            messages.error(request, 'Le numéro de compte {} existe déjà'.format(account_number))
                        elif has_account.get().account_name == account_name:
                            messages.error(request, 'Le nom de compte {} existe déjà'.format(account_name))
                    else:
                        messages.error(request, 'Certaines valeurs sont incorrects')
            path = resolve_url(request.path)
            return redirect(path)
        form = AdditionalAccountingForm()
        form.account_main = main_accounting

        context = {
            'main_accounting': main_accounting,
            'additional_accountings': additional_accountings,
            'form': form,
        }
        return render(request, 'accounting_plan/main_accounting_details.html', context)
    except Main.DoesNotExist:
        return redirect('accounting_index')


@login_required()
def accounting_budget(request):
    year_id = request.session.get('year')
    try:
        fiscal_year = FiscalYear.objects.get(id=year_id)
    except FiscalYear.DoesNotExist:
        return redirect('account_logout')
    try:
        additional_accounts = Additional.objects.filter(account_main__account_type__contains='decaissement').all()

        accounts = list()

        months = months_of_year()
        total_general_budget = 0

        for account in additional_accounts:
            try:
                total_budget = 0
                budgets = Budget.objects.filter(accounting=account, plan_at__year=fiscal_year.year)

                month_budget = list()
                for month in months:
                    budget = budgets.get(plan_at__month=month['id'])
                    total_budget += budget.amount
                    month['balance'] += budget.amount
                    month_budget.append({
                        'id': budget.id,
                        'month': month['name'],
                        'amount': budget.amount
                    })
                accounts.append({
                    'id': account.id,
                    'account_number': account.account_number,
                    'account_name': account.account_name,
                    'budgets': month_budget,
                    'total_budget': total_budget
                })
            except Budget.DoesNotExist:
                pass

        for month in months:
            total_general_budget += month['balance']

        currency = Currency.objects.get(symbol='cdf')

        if request.method == 'POST':

            if request.FILES.get('filebudget'):
                file = request.FILES['filebudget']

                def save_budget(subaccount, rows):
                    for i in range(1, 13):
                        amount = rows[i + 1]
                        plan_at = datetime.date.replace(datetime.date.today(), fiscal_year.year, i, 1)
                        has_budget = Budget.objects.filter(accounting=subaccount, plan_at=plan_at)
                        if not has_budget.exists():
                            ## ToDO verify the type of the amount
                            if type(amount) == np.nan:
                                amount = 0
                            budgetize = Budget(accounting=subaccount, plan_at=plan_at, amount=amount)
                            budgetize.save()

                def loop_upload(dataframe: pd.DataFrame):
                    for data_row in dataframe.values:
                        plan_account_number = data_row[0]

                        try:
                            plan_additional_account = Additional.objects.get(account_number=plan_account_number,
                                                                             account_main__account_type__contains='decaissement')
                            save_budget(plan_additional_account, data_row)
                        except Additional.DoesNotExist:
                            raise NotFound("Ce compte n'existe pas ou n'est pas un compte de decaissement: {}".format(
                                plan_account_number))

                if file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                    path = upload_file(file)

                    df = pd.read_excel(path)

                    loop_upload(df)

                elif file.content_type == 'text/csv':
                    path = upload_file(file)
                    df = pd.read_csv(path, sep=";")

                    loop_upload(df)

                else:
                    raise RequestAborted()

            if 'amount' in request.POST.keys() and 'warning_at' in request.POST.keys():

                for month in range(1, 13):
                    form = BudgetAccountingForm(request.POST)

                    if form.is_valid():
                        pass
                        # budget = form.save(commit=False)
                        # budget.accounting = additional_accounting
                        # budget.plan_at = datetime.date.replace(datetime.date.today(), fy, month, 1)
                        # budget.save()

        budget_form = BudgetAccountingForm()

        # total = total_budget['amount__sum'] * fiscal_year.rate if total_budget['amount__sum'] is not None else 0

        context = {
            'budget_form': budget_form,
            'fiscal_year': fiscal_year,
            'months': months,
            'currencies': currencies,
            'current_checkout': 'images/flags/' + currency.country_code + '.svg',
            'accounts': accounts,
            'total_general_budget': total_general_budget
            # 'budgets': budgets,
            # 'total_budget': total_budget,
            # 'total_budget_converted': total * fiscal_year.rate
        }
        return render(request, 'accounting_plan/budget.html', context)
    except Additional.DoesNotExist:
        return redirect('accounting_index')
    except FiscalYear.DoesNotExist:
        return redirect('accounting_index')


@login_required()
def budget_usage(request, pk):
    year_id = request.session.get('year')
    try:
        fiscal_year = FiscalYear.objects.get(id=year_id)
    except FiscalYear.DoesNotExist:
        return redirect('account_logout')
    try:
        account_additional = Additional.objects.get(id=pk)
        months = list()
        for month in months_of_year():
            budget = Budget.objects.get(accounting=account_additional, plan_at__month=month['id'],
                                        plan_at__year=fiscal_year.year)

            outcomes_in_usd = outcomes_with_subaccount(account_additional, month['id'], fiscal_year.year, 'usd')

            outcome_in_cdf = outcomes_with_subaccount(account_additional, month['id'], fiscal_year.year, 'cdf')

            annote = outcome_in_cdf.annotate(conversion=F('amount') / F('daily_rate__rate'))

            total_usd = 0
            spent = 0
            total_outcomes_usd = outcomes_in_usd.aggregate(Sum('amount'))
            if total_outcomes_usd['amount__sum'] is not None:
                total_usd = total_outcomes_usd['amount__sum']

            if len(annote) > 0:
                total_converted = annote.aggregate(Sum('conversion'))
                spent = round(total_usd + total_converted['conversion__sum'], 2)

            months.append({
                'id': month['id'],
                'name': month['name'],
                'planed': budget.amount.__str__(),
                'spent': spent.__str__(),
                'balance': str(budget.amount - spent)
            })
    except Additional.DoesNotExist:
        return redirect('accounting_budget')
    except Budget.DoesNotExist:
        return redirect('accounting_budget')
    months_json = json.dumps(months)
    context = {
        'months': months,
        'months_json': months_json,
        'account_additional': account_additional,
        'year': fiscal_year.year.__str__()
    }
    return render(request, 'accounting_plan/budget_usage.html', context)


@login_required()
def print_report(request):
    year_id = request.session.get('year')

    """
        here goes the code for the filter
    """
    month_filter = request.GET.get('mois', None)
    is_filter = False
    selected_month = None

    if month_filter:
        is_filter = True
        for month in months_of_year():
            if month['id'] == int(request.GET.get('mois')):
                selected_month = month
                break

    try:
        fiscal_year = FiscalYear.objects.get(id=year_id)
    except FiscalYear.DoesNotExist:
        return redirect('account_logout')

    incomes_report = list()
    incomes_months = months_of_year()
    total_general_incomes = 0
    count_incomes_total_average = 0

    outcomes_report = list()
    outcomes_months = months_of_year()
    total_general_outcomes = 0
    count_outcomes_total_average = 0

    try:
        main_income_accounts = Main.objects.filter(account_type='encaissement').all()
        main_outcome_accounts = Main.objects.filter(account_type='decaissement').all()

        for main_income_account in main_income_accounts:
            report_months = list()
            total_general = 0
            count_incomes_month_average = 0

            for month in incomes_months:
                if month_filter:
                    if selected_month['id'] is not month['id']:
                        continue
                    incomes_usd = Income.objects.filter(accounting_main=main_income_account,
                                                        in_at__month=selected_month['id'],
                                                        in_at__year=fiscal_year.year,
                                                        currency__symbol__icontains='usd')

                    incomes_cdf = Income.objects.filter(accounting_main=main_income_account,
                                                        in_at__month=selected_month['id'],
                                                        in_at__year=fiscal_year.year,
                                                        currency__symbol__icontains='cdf')
                else:
                    incomes_usd = Income.objects.filter(accounting_main=main_income_account, in_at__month=month['id'],
                                                        in_at__year=fiscal_year.year,
                                                        currency__symbol__icontains='usd')

                    incomes_cdf = Income.objects.filter(accounting_main=main_income_account, in_at__month=month['id'],
                                                        in_at__year=fiscal_year.year,
                                                        currency__symbol__icontains='cdf')

                if incomes_cdf.exists() or incomes_usd.exists():
                    count_incomes_total_average += 1
                    count_incomes_month_average += 1

                annote = incomes_cdf.annotate(conversion=F('amount') / F('daily_rate__rate'))

                total_month = 0

                total_incomes_usd = incomes_usd.aggregate(Sum('amount'))
                if total_incomes_usd['amount__sum'] is not None:
                    total_month += total_incomes_usd['amount__sum']

                if len(annote) > 0:
                    total_converted = annote.aggregate(Sum('conversion'))
                    total_month = round(total_month + total_converted['conversion__sum'], 2)
                month['balance'] += total_month
                total_general += total_month
                report_months.append({
                    'id': month['id'],
                    'balance': total_month
                })

            # check if count equal zero, then reset to 1 to avoid DivideByZero error
            if count_incomes_month_average == 0:
                count_incomes_month_average = 1

            incomes_report.append({
                'account_id': main_income_account.id,
                'account_number': main_income_account.account_number,
                'account_name': main_income_account.account_name,
                'months': report_months,
                'total_general': total_general,
                'average': round(total_general / count_incomes_month_average, 2)
            })

        for main_outcome_account in main_outcome_accounts:
            report_months = list()
            total_general = 0
            count_outcomes_month_average = 0

            month_budget = 0

            for month in outcomes_months:
                if month_filter:
                    if selected_month['id'] is not month['id']:
                        continue
                    outcomes_usd = Outcome.objects.filter(accounting_main=main_outcome_account,
                                                          out_at__month=selected_month['id'],
                                                          out_at__year=fiscal_year.year,
                                                          currency__symbol__icontains='usd')

                    outcomes_cdf = Outcome.objects.filter(accounting_main=main_outcome_account,
                                                          out_at__month=selected_month['id'],
                                                          out_at__year=fiscal_year.year,
                                                          currency__symbol__icontains='cdf')

                    budget = Budget.objects.filter(accounting__account_main=main_outcome_account,
                                                   plan_at__month=selected_month['id'])
                    total_budget = budget.aggregate(Sum('amount'))

                    if total_budget['amount__sum'] is not None:
                        month_budget = total_budget['amount__sum']

                else:
                    outcomes_usd = Outcome.objects.filter(accounting_main=main_outcome_account,
                                                          out_at__month=month['id'],
                                                          out_at__year=fiscal_year.year,
                                                          currency__symbol__icontains='usd')

                    outcomes_cdf = Outcome.objects.filter(accounting_main=main_outcome_account,
                                                          out_at__month=month['id'],
                                                          out_at__year=fiscal_year.year,
                                                          currency__symbol__icontains='cdf')

                if outcomes_cdf.exists() or outcomes_usd.exists():
                    count_outcomes_total_average += 1
                    count_outcomes_month_average += 1

                annote = outcomes_cdf.annotate(conversion=F('amount') / F('daily_rate__rate'))

                total_month = 0

                total_outcomes_usd = outcomes_usd.aggregate(Sum('amount'))
                if total_outcomes_usd['amount__sum'] is not None:
                    total_month += total_outcomes_usd['amount__sum']

                if len(annote) > 0:
                    total_converted = annote.aggregate(Sum('conversion'))
                    total_month = round(total_month + total_converted['conversion__sum'], 2)
                month['balance'] += total_month
                total_general += total_month
                gap = month_budget - total_month
                if total_month > month_budget:
                    gap_calculate = total_month - month_budget
                    gap_percent = round((gap_calculate / month_budget) * 100, 2) if month_budget > 0 else 0
                else:
                    gap_percent = 0
                report_months.append({
                    'id': month['id'],
                    'balance': total_month,
                    'budget': month_budget,
                    'budget_gap': round(gap, 2),
                    'budget_gap_percent': gap_percent
                })

            # check if count equal zero, then reset to 1 to avoid DivideByZero error
            if count_outcomes_month_average == 0:
                count_outcomes_month_average = 1

            outcomes_report.append({
                'account_id': main_outcome_account.id,
                'account_number': main_outcome_account.account_number,
                'account_name': main_outcome_account.account_name,
                'months': report_months,
                'total_general': total_general,
                'average': round(total_general / count_outcomes_month_average, 2)
            })
    except Main.DoesNotExist:
        pass

    for month in incomes_months:
        if month_filter:
            if selected_month['id'] is not month['id']:
                continue
            total_general_incomes += month['balance']
        else:
            total_general_incomes += month['balance']

    for month in outcomes_months:
        if month_filter:
            if selected_month['id'] is not month['id']:
                continue
            total_general_outcomes += month['balance']
        else:
            total_general_outcomes += month['balance']

    # check if count equal zero, then reset to 1 to avoid DivideByZero error
    if count_incomes_total_average == 0:
        count_incomes_total_average = 1

    # check if count equal zero, then reset to 1 to avoid DivideByZero error
    if count_outcomes_total_average == 0:
        count_outcomes_total_average = 1

    average_incomes = round(total_general_incomes / count_incomes_total_average, 2)
    average_outcomes = round(total_general_outcomes / count_outcomes_total_average, 2)

    cash_flow = list()
    cash_flow_total = 0
    cash_flow_average = 0

    for i in range(0, 12):

        cash = incomes_months[i]['balance'] - outcomes_months[i]['balance']
        if month_filter:
            if selected_month['id'] is not (i + 1):
                continue
            cash_flow.append(round(cash, 2))
        else:
            cash_flow.append(round(cash, 2))
        cash_flow_total = total_general_incomes - total_general_outcomes
        cash_flow_average = average_incomes - average_outcomes

    context = {
        'incomes_report': incomes_report,
        'incomes_months': incomes_months,
        'total_general_incomes': total_general_incomes,
        'average_incomes': average_incomes,

        'outcomes_report': outcomes_report,
        'outcomes_months': outcomes_months,
        'total_general_outcomes': total_general_outcomes,
        'average_outcomes': average_outcomes,

        'months': months_of_year(),
        'cash_flow': cash_flow,
        'cash_flow_total': round(cash_flow_total, 2),
        'cash_flow_average': round(cash_flow_average, 2),

        'is_filter': is_filter,
        'selected_month': selected_month
    }
    return render(request, 'accounting_plan/print_report.html', context)


## Below is all views concerning apis


@login_required()
@api_view(['GET'])
def api_get_main_account(request):
    main_accountings = Main.objects.all().order_by('account_number')
    serializer = MainSerializer(main_accountings, many=True)
    return Response(serializer.data)


@login_required()
@api_view(['GET'])
def api_get_main_account_debit(request):
    main_accountings = Main.objects.filter(can_debit=True).all().order_by('account_number')
    serializer = MainSerializer(main_accountings, many=True)
    return Response(serializer.data)


@login_required()
@api_view(['POST'])
def api_save_main_account(request):
    account_main = request.data
    serializer = MainSerializer(data=account_main)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': _("Le compte a été ajouté avec succès")}, status=status.HTTP_200_OK)
    else:
        return Response({'message': _("Quelque chose s'est mal passé")}, status=status.HTTP_400_BAD_REQUEST)


@login_required()
@api_view(['POST'])
def api_update_main_account(request):
    account_id = request.data['id']
    account_main = Main.objects.get(id=account_id)
    serializer = MainSerializer(account_main, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': _("La modification a été effectuée avec succès")}, status=status.HTTP_200_OK)
    else:
        return Response({'message': _("Quelque chose s'est mal passé")}, status=status.HTTP_400_BAD_REQUEST)


@login_required()
@api_view(['POST'])
def api_delete_main_account(request):
    account_id = request.data['id']
    account_main = Main.objects.get(id=account_id)
    account_main.delete()
    return Response({'message': _("Le compte a été supprimé avec succès")}, status=status.HTTP_200_OK)


@login_required()
@api_view(['GET'])
def api_get_subaccount_filter_main(request, account_id):
    main_accountings = Additional.objects.filter(account_main__id=account_id).all().order_by('account_number')
    serializer = AdditionalSerializer(main_accountings, many=True)

    return Response(serializer.data)


@login_required()
@api_view(['GET'])
def api_get_subaccount_debit_filter_main(request, account_id):
    main_accountings = Additional.objects.filter(account_main__id=account_id,
                                                 account_main__can_debit=True).all().order_by('account_number')
    serializer = AdditionalSerializer(main_accountings, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def api_get_accounting_main_by_type(request, account_type):
    main = Main.objects.filter(account_type=account_type).all()
    serializer = MainSerializer(main, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@login_required()
def api_get_plans(request):
    user = request.user

    try:
        Plan.manager.get_tree()
        return Response(Plan.manager.get_tree())
    except Plan.DoesNotExist as e:
        context = {
            'message': _("Aucun plan comptable n'existe pour cette entreprise")
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def api_get_accounts_by_category(request):
    try:
        query = request.GET.get('categories').split(',')
        categories = PlanCategory.objects.filter(name__in=query).all()
        filters = list()

        for category in categories:
            filters.append(category.id)

            for item in category.get_children():
                filters.append(item.id)

        accounts = Plan.objects.filter(category__in=filters).all()

        return Response(accounts.values('id', 'account_number', 'account_name', 'category__name',
                                        'currency__name', 'allow_lettering'))
    except Plan.DoesNotExist as e:
        context = {
            'message': _("Aucun plan comptable n'existe")
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def api_get_accounts(request, account_id):
    try:
        journal = Journal.objects.get(id=account_id)
        root = Plan.objects.get(id=journal.account.id)
        accounts = Plan.objects.filter(path__startswith=root.path).all()

        return Response(accounts.values('id', 'account_number', 'account_name', 'category__name',
                                        'currency__name', 'allow_lettering'))

    except Journal.DoesNotExist:
        context = {
            'message': _("Ce module n'existe pas")
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)


# create an accounting plan
@api_view(['POST'])
@login_required()
def api_create_plan(request):
    user = request.user

    serializer = PlanSerializer(data=request.data)

    if serializer.is_valid():
        try:
            account_number = serializer.validated_data['account_number']
            account_name = serializer.validated_data['account_name']
            parent = request.data['parent']
            root_node = Plan.objects.get(id=parent, depth=1)
            custom_plan = Plan(account_number=account_number, account_name=account_name)
            root_node.add_child(instance=custom_plan)
            context = {'message': "Plan comptable ajouté avec succès"}
            return Response(context, status=status.HTTP_201_CREATED)
        except Plan.DoesNotExist:
            context = {'message': "Aucun plan comptable parent n'a été trouvé"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            context = {'message': e.__str__()}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            context = {'message': e.__str__()}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            context = {'message': 'une clé manquante: {}'.format(e.__str__())}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors)


@api_view(['PUT'])
@login_required()
def api_update_plan(request):
    user = request.user

    try:
        plan_id = request.data['id']
        plan = Plan.objects.get(id=plan_id)

        serializer = PlanSerializer(plan, data=request.data, partial=True)
        if serializer.is_valid():
            if serializer.validated_data['account_number'] is None or serializer.validated_data['account_name'] is None:
                account_number = serializer.validated_data['account_number']
                account_name = serializer.validated_data['account_name']

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except IntegrityError as e:
        context = {'message': e.__str__()}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    except ValueError as e:
        context = {'message': e.__str__()}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    except KeyError as e:
        context = {
            'message': 'une clé manquante: {}'.format(e.__str__())
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    except Plan.DoesNotExist:
        context = {
            'message': "Ce compte n'existe pas dans votre plan comptable"
        }
        return Response(context, status=status.HTTP_404_NOT_FOUND)
    except ValidationError as e:
        context = {'message': e.__str__()}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@login_required()
def api_delete_plan(request):
    user = request.user

    try:
        plan_id = request.data['id']
        plan = Plan.objects.get(id=plan_id)

        context = {
            'message': 'Le compte {} - {} a été supprimé de votre plan comptable avec succès'.format(
                plan.account_number,
                plan.account_name)
        }
        plan.delete()
        return Response(context, status=status.HTTP_200_OK)
    except KeyError as e:
        context = {
            'message': 'une clé manquante: {}'.format(e.__str__())
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    except Plan.DoesNotExist as e:
        context = {
            'message': "Ce compte n'existe pas dans votre plan comptable"
        }
        return Response(context, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@login_required()
def api_upload_plan(request):
    user = request.user

    try:
        file = request.data['file']

        if type(file) == str:
            return Response({'message': _("aucun fichier n'a été envoyé")}, status=status.HTTP_404_NOT_FOUND)

        if file.content_type == 'text/csv':

            upload = upload_file(file)

            df = pd.read_csv(upload['path'], sep=';')

            count_success = 0
            count_fail = df.shape[0]

            report = {
                'load_success': list(),
            }

            for custom_plan in df.values:
                if len(custom_plan) >= 2:
                    custom_account_number = str(custom_plan[0])
                    custom_account_name = str(custom_plan[1])

                    sub_accountings = Plan.objects.filter(depth=2).all()

                    for sub_accounting in sub_accountings:
                        if custom_account_number.startswith(sub_accounting.account_number):
                            count_success += 1
                            count_fail -= 1
                            try:
                                sub_accounting.add_child(coding=custom_account_number, title=custom_account_name,
                                                         load_from='csv')
                            except IntegrityError as e:
                                context = {'message': e.__str__()}
                                return Response(context, status=status.HTTP_400_BAD_REQUEST)
                            report['load_success'].append({'account_number': custom_account_number,
                                                           'account_name': custom_account_number})
                            break
                else:
                    break
            report['count_success'] = count_success
            report['count_fail'] = count_fail
            fs.delete(upload['name'])
            return Response(report)
        elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':

            upload = upload_file(file)

            df = pd.read_excel(upload['path'])

            count_success = 0
            count_fail = df.shape[0]

            report = {
                'load_success': list(),
            }

            for custom_plan in df.values:
                if len(custom_plan) >= 2:
                    custom_account_number = str(custom_plan[0])
                    custom_account_name = str(custom_plan[1])

                    sub_accountings = Plan.objects.filter(depth=2).all()

                    for sub_accounting in sub_accountings:
                        if custom_account_number.startswith(sub_accounting.account_number):
                            count_success += 1
                            count_fail -= 1
                            try:
                                sub_accounting.add_child(coding=custom_account_number, title=custom_account_name,
                                                         load_from='excel')
                            except IntegrityError as e:
                                context = {'message': e.__str__()}
                                return Response(context, status=status.HTTP_400_BAD_REQUEST)
                            report['load_success'].append({'account_number': custom_account_number,
                                                           'account_name': custom_account_name})
                            break
                else:
                    break
            report['count_success'] = count_success
            report['count_fail'] = count_fail
            fs.delete(upload['name'])
            return Response(report)
        raise NotAcceptable(_("Ce type de fichier n'est pas acceptable. envoyez un fichier valide en excel ou csv"))

    except KeyError as e:
        context = {'message': 'une clé manquante: {}'.format(e.__str__())}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@login_required()
def api_load_ohada(request):
    try:
        df = pd.read_csv('static/plan_comptable.csv', sep=';', index_col=False)
        df['account_number'] = df['account_number'].astype(str)

        for value in df.values:
            coding = value[0]
            title = value[1]

            if len(coding) == 2:
                if int(coding) < 20 or int(coding) == 40:
                    group = 'passif'
                elif 20 <= int(coding) < 60:
                    group = 'actif'
                elif 60 <= int(coding) < 70:
                    group = 'charge'
                elif 70 <= int(coding) < 80:
                    group = 'produit'
                else:
                    group = None
                try:
                    Plan.add_root(coding=coding, title=title, group=group, load_from='csv')
                except IntegrityError as e:
                    continue
            else:
                nodes = Plan.objects.filter(depth=1, company__isnull=True).all()

                for node in nodes:
                    if node.is_root():
                        if str(coding).startswith(node.coding):
                            try:

                                child = Plan(coding=coding, title=title, load_from='csv')
                                node.add_child(instance=child)
                            except IntegrityError as e:
                                continue

        return Response({'message': _("chargement réussi!")})
    except MultiValueDictKeyError as e:
        context = {'message': 'une clé manquante: {}'.format(e.__str__())}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    except DataError as e:
        return Response(_("Quelque chose s'est mal passé! {}".format(e.__str__())),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
