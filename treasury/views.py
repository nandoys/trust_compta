from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

from .forms import OutcomeForm, Currency, CurrencyDailyRate, OutcomeModelForm, IncomeForm
from .models import Outcome
from accounting_plan.models import Main, Additional, Adjunct, Budget, FiscalYear


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

    incomes_obj = Outcome.objects.filter(currency=currency, out_at__year=fiscal_year.year).all()
    total_checkout = incomes_obj.aggregate(Sum('amount'))

    income_form = IncomeForm()

    context = {
        'fiscal_year': fiscal_year,
        'income_form': income_form,
        'currencies': currencies,
        'currency': currency,
        'current_checkout': 'images/flags/' + currency.country_iso + '.svg',
        'incomes_obj': incomes_obj,
        'total_checkout': total_checkout
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
    outcomes_obj = Outcome.objects.filter(currency=currency, out_at__year=fiscal_year.year).all()
    total_checkout = outcomes_obj.aggregate(Sum('amount'))

    if request.method == 'POST':

        form = OutcomeModelForm(request.POST)

        if form.is_valid():
            outcome = form.save(commit=False)
            outcome.currency = currency

            has_accounting_ajunct = request.POST.get('accounting_adjunct', None)

            if has_accounting_ajunct is not None:
                account_adjunct = Adjunct.objects.get(id=request.POST['accounting_adjunct'])
                outcome.accounting_adjunct = account_adjunct

            if currency.is_local:
                daily_rate = CurrencyDailyRate.objects.get(to_currency=currency, in_use=True)
                outcome.daily_rate = daily_rate

            outcome.save()

    outcome_form = OutcomeForm()

    context = {
        'fiscal_year': fiscal_year,
        'outcome_form': outcome_form,
        'currencies': currencies,
        'currency': currency,
        'current_checkout': 'images/flags/' + currency.country_iso + '.svg',
        'outcomes': outcomes_obj,
        'total_checkout': total_checkout
    }
    return render(request, 'treasury/outcomes.html', context)


def accounting_additional(request):
    accounting_main_id = request.GET.get('accounting_main_id')
    accounting_main = Main.objects.get(id=accounting_main_id)
    accountings_additional = Additional.objects.filter(account_main=accounting_main).all()

    return JsonResponse(list(accountings_additional.values('id', 'account_name')), safe=False)


def accounting_adjunct(request):
    year = request.GET.get('fiscal_year')
    fiscal_year = FiscalYear.objects.get(year=year)

    accounting_additional_id = request.GET.get('accounting_additional_id')
    accounting_additional = Additional.objects.get(id=accounting_additional_id)
    accountings_adjunct = Adjunct.objects.filter(account_additional=accounting_additional).all()

    # budget_warn = fiscal_year.budget_set.get(accounting=accounting_additional).warning_at

    # print(budget_warn)

    return JsonResponse(list(accountings_adjunct.values('id', 'adjunct_account_name')), safe=False)
