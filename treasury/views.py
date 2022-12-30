from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum

from .forms import OutcomeForm, Currency, CurrencyDailyRate
from .models import Outcome
from accounting_plan.models import Additional, Adjunct, Budget, FiscalYear


# Create your views here.


def index(request):
    return render(request, 'treasury/template.html')


def incomes(request):
    return render(request, 'treasury/incomes.html')


def outcomes(request, symbol, year):
    fiscal_year = FiscalYear.objects.get(year=year)
    currencies = list()
    for currency in Currency.objects.all():
        currencies.append({
            'name': currency.name,
            'symbol_iso': currency.symbol_iso,
            'country_iso': currency.country_iso,
            'flag': 'images/flags/'+currency.country_iso+'.svg'
        })
    currency = Currency.objects.get(symbol_iso=symbol)
    outcomes_obj = Outcome.objects.filter(currency=currency, out_at__year=year).all()
    total_checkout = outcomes_obj.aggregate(Sum('amount'))

    if request.method == 'POST':
        tag_id = request.POST['tag']
        tag = Adjunct.objects.get(id=tag_id)

        form = OutcomeForm(request.POST)

        if form.is_valid():
            outcome = form.save(commit=False)
            outcome.currency = currency
            outcome.tag = tag

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
        'current_checkout': 'images/flags/'+currency.country_iso+'.svg',
        'outcomes': outcomes_obj,
        'total_checkout': total_checkout
    }
    return render(request, 'treasury/outcomes.html', context)


def tags(request):
    accounting_id = request.GET.get('accounting_id')
    accounting = Additional.objects.get(id=accounting_id)
    tags = Adjunct.objects.filter(account_additional=accounting).all()

    # Outcome.objects.filter(accounting=accounting, yea)

    return JsonResponse(list(tags.values('id', 'adjunct_account_name')), safe=False)
