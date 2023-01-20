import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Main, Additional, FiscalYear, Budget
from .forms import MainAccountingForm, AdditionalAccountingForm, AdjunctAccountingForm, BudgetAccountingForm, \
    FiscalYearForm
from .serializer import MainSerializer

from treasury.models import Currency, Income, Outcome

# Create your views here.

months = [
    {'id': 1, 'name': 'Janvier', 'balance': {}}, {'id': 2, 'name': 'Février', 'balance': {}},
    {'id': 3, 'name': 'Mars', 'balance': {}},
    {'id': 4, 'name': 'Avril', 'balance': {}}, {'id': 5, 'name': 'Mai', 'balance': {}},
    {'id': 6, 'name': 'Juin', 'balance': {}},
    {'id': 7, 'name': 'Juillet', 'balance': {}}, {'id': 8, 'name': 'Août', 'balance': {}},
    {'id': 9, 'name': 'Septembre', 'balance': {}},
    {'id': 10, 'name': 'Octobre', 'balance': {}}, {'id': 11, 'name': 'Novembre', 'balance': {}},
    {'id': 12, 'name': 'Décembre', 'balance': {}}
]

currencies = list()
for curr in Currency.objects.all():
    currencies.append({
        'name': curr.name,
        'symbol_iso': curr.symbol_iso,
        'country_iso': curr.country_iso,
        'flag': 'images/flags/' + curr.country_iso + '.svg'
    })


@login_required()
def index(request):
    year_id = request.session.get('year')
    try:
        fiscal_year = FiscalYear.objects.get(id=year_id)
    except FiscalYear.DoesNotExist:
        return redirect('account_logout')

    currency_cdf = Currency.objects.get(symbol_iso='cdf')
    currency_usd = Currency.objects.get(symbol_iso='usd')

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
        'months': months,
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

    try:
        fiscal_year = FiscalYear.objects.get(id=year_id)
        currency = Currency.objects.get(symbol_iso=symbol)
    except FiscalYear.DoesNotExist:
        return redirect('account_logout')
    except Currency.DoesNotExist:
        return redirect('accounting_plan_index')

    main_acc_outcomes = Main.objects.filter(account_type='decaissement').all()

    main_reports = list()

    for main_acc_outcome in main_acc_outcomes:
        total_outcomes = main_acc_outcome.outcome_set.filter(currency=currency, out_at__year=fiscal_year.year).all()
        report_outcomes = total_outcomes.aggregate(Sum('amount'))
        balance_main_report = 0

        additional_acc_outcomes = main_acc_outcome.additional_set.all()

        additional_reports = list()
        for additional_acc_outcome in additional_acc_outcomes:
            total_additional_acc_outcomes = additional_acc_outcome.outcome_set.filter(currency=currency,
                                                                                      out_at__year=fiscal_year.year).all()
            report_additional_acc_outcomes = total_additional_acc_outcomes.aggregate(Sum('amount'))
            balance_additional_report = 0

            adjunct_acc_outcomes = additional_acc_outcome.adjunct_set.all()

            adjunct_reports = list()
            for adjunct_acc_outcome in adjunct_acc_outcomes:
                total_adjunct_acc_outcomes = adjunct_acc_outcome.outcome_set.filter(currency=currency,
                                                                                    out_at__year=fiscal_year.year).all()
                report_adjunct_acc_outcomes = total_adjunct_acc_outcomes.aggregate(Sum('amount'))
                balance_adjunct_report = 0

                if report_adjunct_acc_outcomes['amount__sum'] is not None:
                    balance_adjunct_report = report_adjunct_acc_outcomes['amount__sum']

                adjunct_reports.append({
                    'acc_name': adjunct_acc_outcome.adjunct_account_name,
                    'balance': balance_adjunct_report
                })

            if report_additional_acc_outcomes['amount__sum'] is not None:
                balance_additional_report = report_additional_acc_outcomes['amount__sum']

            additional_reports.append({
                'acc_name': additional_acc_outcome.account_name,
                'acc_number': additional_acc_outcome.account_number,
                'balance': balance_additional_report,
                'acc_adjunct': adjunct_reports
            })

        if report_outcomes['amount__sum'] is not None:
            balance_main_report = report_outcomes['amount__sum']

        main_reports.append({
            'acc_name': main_acc_outcome.account_name,
            'acc_number': main_acc_outcome.account_number,
            'balance': balance_main_report,
            'acc_additionals': additional_reports
        })

    context = {
        'reports': main_reports
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
    for m in months:
        if m.get('id') == get_month:
            selected_month = m

    currency = Currency.objects.get(symbol_iso='usd')

    if request.method == 'POST':

        if 'delete-item' in request.POST.keys():
            main_accounting = Main.objects.filter(id=request.POST['delete-item'])
            main_accounting.delete()
        else:
            accounting_item = MainAccountingForm(request.POST)
            if accounting_item.is_valid():
                accounting_item.save()
                messages.success(request, 'Compte ajouté avec succès')
            else:
                messages.error(request, 'Les valeurs envoyées sont incorrectes')

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
        'current_checkout': 'images/flags/' + currency.country_iso + '.svg',
    }
    return render(request, 'accounting_plan/index.html', context)


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
                accounting_item = AdditionalAccountingForm(request.POST)

                if accounting_item.is_valid():
                    instance = accounting_item.save(commit=False)
                    instance.account_main = main_accounting
                    instance.save()
                    messages.success(request, 'Compte ajouté avec succès')
                else:
                    messages.error(request, 'Les valeurs envoyées sont incorrectes')

        form = AdditionalAccountingForm()
        form.account_main = main_accounting

        context = {
            'main_accounting': main_accounting,
            'additional_accountings': additional_accountings,
            'form': form,
        }
        return render(request, 'accounting_plan/main_accounting_details.html', context)
    except Main.DoesNotExist:
        return redirect('accounting_plan_index')


@login_required()
def accounting_budget(request, pk, fy):
    try:
        fiscal_years = FiscalYear.objects.all()
        fiscal_year = FiscalYear.objects.get(year=fy)
        additional_accounting = Additional.objects.get(id=pk)
        budgets = Budget.objects.filter(accounting=additional_accounting, plan_at__year=fiscal_year.year)

        total_budget = budgets.aggregate(Sum('amount'))

        currency = Currency.objects.get(symbol_iso='cdf')

        if request.method == 'POST':

            if 'year' in request.POST.keys() and 'rate' in request.POST.keys():
                form = FiscalYearForm(request.POST)

                if form.is_valid():
                    form.save()
            elif 'amount' in request.POST.keys() and 'warning_at' in request.POST.keys():

                for month in range(1, 13):
                    form = BudgetAccountingForm(request.POST)

                    if form.is_valid():
                        budget = form.save(commit=False)
                        budget.accounting = additional_accounting
                        budget.plan_at = datetime.date.replace(datetime.date.today(), fy, month, 1)
                        budget.save()

            elif 'adjunct_account_name' in request.POST.keys():
                form = AdjunctAccountingForm(request.POST)

                if form.is_valid():
                    adjunct = form.save(commit=False)
                    adjunct.account_additional = additional_accounting
                    adjunct.save()

        budget_form = BudgetAccountingForm()
        adjunct_form = AdjunctAccountingForm()
        fiscal_year_form = FiscalYearForm()
        total = total_budget['amount__sum'] * fiscal_year.rate if total_budget['amount__sum'] is not None else 0

        context = {
            'budget_form': budget_form,
            'adjunct_form': adjunct_form,
            'fiscal_year_form': fiscal_year_form,
            'fiscal_years': fiscal_years,
            'fiscal_year': fiscal_year,
            'currencies': currencies,
            'current_checkout': 'images/flags/' + currency.country_iso + '.svg',
            'additional_accounting': additional_accounting,
            'budgets': budgets,
            'total_budget': total_budget,
            'total_budget_converted': total * fiscal_year.rate
        }
        return render(request, 'accounting_plan/accounting_budget.html', context)
    except Additional.DoesNotExist:
        return redirect('accounting_plan_index')
    except FiscalYear.DoesNotExist:
        return redirect('accounting_plan_index')


@api_view(['GET'])
def api_get_accounting_main_by_type(request, account_type):
    main = Main.objects.filter(account_type=account_type).all()
    serializer = MainSerializer(main, many=True)

    return Response(serializer.data)
