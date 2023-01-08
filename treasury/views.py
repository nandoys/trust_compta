from django.shortcuts import render, redirect, reverse, resolve_url
from django.http import JsonResponse
from django.db.models import Sum
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounting_plan.models import Main, Additional, Adjunct, Budget, FiscalYear
from .forms import OutcomeForm, OutcomeModelForm, IncomeForm, IncomeModelForm
from .models import Outcome, Income, Currency, CurrencyDailyRate
from .serializer import IncomeSerializer, OutcomeSerializer


# Create your views here.
@login_required()
def index(request):
    return render(request, 'treasury/template.html')


@login_required()
def incomes(request, symbol):
    year_id = request.session.get('year')
    fiscal_year = FiscalYear.objects.get(id=year_id)

    currencies = list()
    for currency in Currency.objects.all():
        currencies.append({
            'name': currency.name,
            'symbol_iso': currency.symbol_iso,
            'country_iso': currency.country_iso,
            'flag': 'images/flags/' + currency.country_iso + '.svg'
        })
    currency = Currency.objects.get(symbol_iso=symbol)

    incomes_obj = Income.objects.filter(currency=currency, in_at__year=fiscal_year.year).all()
    outcomes_obj = Outcome.objects.filter(currency=currency, out_at__year=fiscal_year.year).all()

    total_checkout_income = incomes_obj.aggregate(Sum('amount'))

    total_checkout_outcome = outcomes_obj.aggregate(Sum('amount'))

    if total_checkout_income['amount__sum'] is None:
        total_checkout_income['amount__sum'] = 0
    elif total_checkout_outcome['amount__sum'] is None:
        total_checkout_outcome['amount__sum'] = 0

    balance = total_checkout_income['amount__sum'] - total_checkout_outcome['amount__sum']

    if request.method == 'POST':

        if request.POST.get('update_record_id'):
            pk = request.POST['update_record_id']
            income = Income.objects.get(id=pk)
            form = IncomeModelForm(request.POST, instance=income)

            if form.is_valid():
                income = form.save(commit=False)
                income.slip_number = request.POST['slip_number']
                income.more = request.POST['more']
                form.save()
            path = resolve_url(request.path)
            return redirect(path)

        form = IncomeModelForm(request.POST)

        if form.is_valid():
            income = form.save(commit=False)
            income.currency = currency
            income.slip_number = request.POST['slip_number']
            income.more = request.POST['more']

            has_accounting_additional = request.POST.get('accounting_additional', None)
            has_accounting_ajunct = request.POST.get('accounting_adjunct', None)

            if has_accounting_additional is not None:
                account_additional = Additional.objects.get(id=request.POST['accounting_additional'])
                income.accounting_additional = account_additional

            if has_accounting_ajunct is not None:
                account_adjunct = Adjunct.objects.get(id=request.POST['accounting_adjunct'])
                income.accounting_adjunct = account_adjunct

            if currency.is_local:
                daily_rate = CurrencyDailyRate.objects.get(to_currency=currency, in_use=True)
                income.daily_rate = daily_rate
            try:
                income.save()
            except IntegrityError as error:
                if "slip_number" in error.__str__():
                    messages.error(request, 'Ce numéro de bordereau [{}] existe déjà'.format(income.slip_number))

            path = resolve_url(request.path)
            return redirect(path)

    income_form = IncomeForm()

    context = {
        'fiscal_year': fiscal_year,
        'income_form': income_form,
        'currencies': currencies,
        'currency': currency,
        'current_checkout': 'images/flags/' + currency.country_iso + '.svg',
        'incomes': incomes_obj,
        'total_checkout': total_checkout_income,
        'balance': balance
    }
    return render(request, 'treasury/incomes.html', context)


@login_required()
def outcomes(request, symbol):
    year_id = request.session.get('year')
    fiscal_year = FiscalYear.objects.get(id=year_id)

    currencies = list()
    for currency in Currency.objects.all():
        currencies.append({
            'name': currency.name,
            'symbol_iso': currency.symbol_iso,
            'country_iso': currency.country_iso,
            'flag': 'images/flags/' + currency.country_iso + '.svg'
        })
    currency = Currency.objects.get(symbol_iso=symbol)

    incomes_obj = Income.objects.filter(currency=currency, in_at__year=fiscal_year.year).all()
    outcomes_obj = Outcome.objects.filter(currency=currency, out_at__year=fiscal_year.year).all()

    total_checkout_income = incomes_obj.aggregate(Sum('amount'))

    total_checkout_outcome = outcomes_obj.aggregate(Sum('amount'))

    if total_checkout_income['amount__sum'] is None:
        total_checkout_income['amount__sum'] = 0
    elif total_checkout_outcome['amount__sum'] is None:
        total_checkout_outcome['amount__sum'] = 0

    balance = total_checkout_income['amount__sum'] - total_checkout_outcome['amount__sum']

    if request.method == 'POST':

        if request.POST.get('update_record_id'):
            pk = request.POST['update_record_id']
            outcome = Outcome.objects.get(id=pk)
            form = OutcomeModelForm(request.POST, instance=outcome)

            if form.is_valid():
                form.save()
            path = resolve_url(request.path)
            return redirect(path)

        form = OutcomeModelForm(request.POST)

        if form.is_valid():
            outcome = form.save(commit=False)

            if outcome.amount > balance:
                messages.error(request,
                               'Votre solde est insuffisant pour éffectuer cette opération! [{} {}]'.format(
                                   balance, currency.symbol_iso))
                path = resolve_url(request.path)
                return redirect(path)

            outcome.currency = currency

            has_accounting_adjunct = request.POST.get('accounting_adjunct', None)

            if has_accounting_adjunct is not None:
                account_adjunct = Adjunct.objects.get(id=request.POST['accounting_adjunct'])
                outcome.accounting_adjunct = account_adjunct

            if currency.is_local:
                daily_rate = CurrencyDailyRate.objects.get(to_currency=currency, in_use=True)
                outcome.daily_rate = daily_rate
            try:
                outcome.save()
            except IntegrityError as error:
                if "slip_number" in error.__str__():
                    messages.error(request, 'Ce numéro de bordereau [{}] existe déjà'.format(outcome.slip_number))

            path = resolve_url(request.path)
            return redirect(path)
        if form.has_error('slip_number'):
            messages.error(request, 'Ce numéro de bordereau [{}] existe déjà'.format(request.POST['slip_number']))
            path = resolve_url(request.path)
            return redirect(path)
    outcome_form = OutcomeForm()

    context = {
        'fiscal_year': fiscal_year,
        'outcome_form': outcome_form,
        'currencies': currencies,
        'currency': currency,
        'current_checkout': 'images/flags/' + currency.country_iso + '.svg',
        'outcomes': outcomes_obj,
        'total_checkout': total_checkout_outcome,
        'balance': balance
    }
    return render(request, 'treasury/outcomes.html', context)


def accounting_additional(request):
    accounting_main_id = request.GET.get('accounting_main_id')
    accounting_main = Main.objects.get(id=accounting_main_id)
    accountings_additional = Additional.objects.filter(account_main=accounting_main).all()

    return JsonResponse(list(accountings_additional.values('id', 'account_name')), safe=False)


def accounting_adjunct(request):
    # year = request.GET.get('fiscal_year')
    # fiscal_year = FiscalYear.objects.get(year=year)

    accounting_additional_id = request.GET.get('accounting_additional_id')
    accounting_additional = Additional.objects.get(id=accounting_additional_id)
    accountings_adjunct = Adjunct.objects.filter(account_additional=accounting_additional).all()

    # budget_warn = fiscal_year.budget_set.get(accounting=accounting_additional).warning_at


    return JsonResponse(list(accountings_adjunct.values('id', 'adjunct_account_name')), safe=False)


def edit_income(request, pk):
    income = Income.objects.get(id=pk)
    income_serializer = IncomeSerializer(income, many=False)
    return JsonResponse(income_serializer.data, safe=False)


def edit_outcome(request, pk):
    outcome = Outcome.objects.get(id=pk)
    outcome_serializer = OutcomeSerializer(outcome, many=False)
    return JsonResponse(outcome_serializer.data, safe=False)
