import datetime

from django.shortcuts import render, redirect, resolve_url
from django.http import JsonResponse
from django.db.models import Sum
from django.db.utils import IntegrityError
from django.utils.formats import localize
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from accounting.models import Main, Additional, Adjunct, FiscalYear, Budget, Monitoring, Plan
from billing.models import Partner
from settings.models import Journal
from utils.token import set_auth_token

from .forms import OutcomeForm, OutcomeModelForm, IncomeForm, IncomeModelForm
from .models import Outcome, Income, Currency, CurrencyDailyRate, AccountingEntry, Statement
from .serializer import IncomeSerializer, OutcomeSerializer

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
        'symbol': curr.symbol,
        'country_code': curr.country_code,
        'flag': 'images/flags/' + curr.country_code + '.svg'
    })


# Create your views here.
@login_required()
def index(request):
    year_id = request.session.get('year')
    try:
        fiscal_year = FiscalYear.objects.get(id=year_id)
    except FiscalYear.DoesNotExist:
        return redirect('account_logout')

    for month in months:
        for currency in currencies:
            currency = Currency.objects.get(symbol=currency['symbol'])
            incomes_obj = Income.objects.filter(currency=currency, in_at__month=month['id'],
                                                in_at__year=fiscal_year.year).all()
            outcomes_obj = Outcome.objects.filter(currency=currency, out_at__month=month['id'],
                                                  out_at__year=fiscal_year.year).all()

            total_checkout_income = incomes_obj.aggregate(Sum('amount'))
            balance_income = 0

            total_checkout_outcome = outcomes_obj.aggregate(Sum('amount'))
            balance_outcome = 0

            if total_checkout_income['amount__sum'] is not None:
                balance_income = total_checkout_income['amount__sum']

            if total_checkout_outcome['amount__sum'] is not None:
                balance_outcome = total_checkout_outcome['amount__sum']

            balance = balance_income - balance_outcome

            month['balance'][currency.symbol] = balance

    context = {
        'months': months,
        'currencies': currencies,
        'fiscal_year': fiscal_year.year
    }
    return render(request, 'treasury/dashboard.html', context)


@login_required()
def checkout(request, symbol, year, month, module_id):
    year_id = request.session.get('year')

    token = request.COOKIES.get('access_token')

    modules = Journal.objects.all()
    try:
        fiscal_year = FiscalYear.objects.get(id=year_id)
    except FiscalYear.DoesNotExist:
        return redirect('account_logout')
    selected_month = dict()

    for m in months:
        if m.get('id') == month:
            selected_month = m

    currency = Currency.objects.get(symbol=symbol)

    incomes_total = Income.objects.filter(currency=currency).all()
    outcomes_total = Outcome.objects.filter(currency=currency).all()

    incomes_obj = Income.objects.filter(currency=currency, in_at__month=selected_month.get('id'),
                                        in_at__year=fiscal_year.year).all()

    total_checkout_income = incomes_total.aggregate(Sum('amount'))
    balance_income = 0

    total_checkout_outcome = outcomes_total.aggregate(Sum('amount'))
    balance_outcome = 0

    if total_checkout_income['amount__sum'] is not None:
        balance_income = total_checkout_income['amount__sum']

    if total_checkout_outcome['amount__sum'] is not None:
        balance_outcome = total_checkout_outcome['amount__sum']

    balance = balance_income - balance_outcome

    if request.method == 'POST':

        if request.POST.get('edit_record_id'):
            pk = request.POST['edit_record_id']

            income_data = Income.objects.get(id=pk)
            form = IncomeModelForm(request.POST, instance=income_data)

            if form.is_valid():
                income = form.save(commit=False)
                income.slip_number = request.POST['slip_number']
                income.more = request.POST['more']
                form.save()
                messages.success(request,
                                 'Recette pour le compte [{}] du [{}] a été modifiée avec succès. Montant: [{}] [{}]'.format(
                                     income.accounting_main, localize(income_data.in_at, use_l10n=True), income.amount,
                                     income.currency.symbol))
            path = resolve_url(request.path)
            return redirect(path)

        if request.POST.get('remove_record_id'):
            pk = request.POST['remove_record_id']
            income_data = Income.objects.get(id=pk)

            try:
                income_data.delete()
                messages.success(request,
                                 'Recette pour le compte [{}] du [{}] / [{}]  a été supprimée avec succès. Montant: [{}] [{}]'.format(
                                     income_data.accounting_main, localize(income_data.in_at, use_l10n=True),
                                     income_data.more, income_data.amount, income_data.currency.symbol))
                path = resolve_url(request.path)
                return redirect(path)
            except:
                pass

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
                messages.success(request,
                                 'Recette pour le compte [{}] a été enregistrée avec succès. Montant: [{}] [{}]'.format(
                                     income.accounting_main, income.amount, income.currency.symbol))
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
        'current_checkout': 'images/flags/' + currency.country_code + '.svg',
        'modules': modules,
        'selected_month': selected_month,
        'incomes': incomes_obj,
        'total_checkout': total_checkout_income,
        'balance': balance
    }
    response = render(request, 'treasury/incomes.html', context)

    # verify if there is no token and create one
    if not token:
        set_auth_token(request, response)

    # verify if the existing token is invalid then create one
    try:
        JWT_authenticator = JWTAuthentication()
        JWT_authenticator.get_validated_token(token)
    except InvalidToken:
        set_auth_token(request, response)

    return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_get_incomes(request):

    statement_id = request.GET.get('statementId')
    entries = AccountingEntry.objects.filter(ref_statement__id=statement_id).all()

    return Response(
        entries.values('id', 'account__account_number', 'account__account_name', 'date_at', 'label', 'debit', 'credit', 'is_verified'))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_save_statement(request):
    try:
        data = request.data
        user = request.user
        transaction_date = data['dateOperation']
        partner = Partner.objects.get(id=data['partner']) if data['partner'] != '' else None
        label = data['label']
        account = data['account']
        currency = data['currency']
        rate = data['rate'] if data['rate'] != '' else 1
        amount = data['amount']

        statement = Statement(transaction_at=transaction_date, partner=partner, reference=data['reference'],
                              label=label,
                              account_id=account, currency_id=currency, rate=rate, amount=amount)

        statement.save()

        # add accounting entry for the statement
        accounting_entry = AccountingEntry(account_id=account, currency_id=currency, rate=rate, ref_statement=statement,
                                           label=label, partner=partner, date_at=transaction_date, debit=amount,
                                           credit=0, done_by=user)

        accounting_entry.save()

        context = {'message': "Votre relevé a été ajouté avec succès!"}

        return Response(context, status=status.HTTP_201_CREATED)
    except BaseException as error:
        print(error)
        return Response({'message': _("Quelque chose s'est mal passé")}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_get_statements(request):
    statements = Statement.objects.all()
    return Response(statements.values('id', 'label', 'reference', 'transaction_at', 'currency__name', 'currency_id',
                                      'currency__symbol', 'amount', 'rate', 'account__account_number',
                                      'account__account_name',
                                      'account_id'))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_get_currencies(request):
    data = list()
    all_currency = Currency.objects.all()

    for currency in all_currency:
        daily = None
        if not currency.is_local:
            daily = CurrencyDailyRate.objects.get(to_currency=currency, in_use=True)
        data.append(
            {'id': currency.id, 'name': currency.name, 'symbol': currency.symbol, 'is_local': currency.is_local,
             'rate': daily.rate if daily is not None else None})
    return Response(data)


@login_required()
def outcomes(request, symbol, month):
    year_id = request.session.get('year')
    try:
        fiscal_year = FiscalYear.objects.get(id=year_id)
    except FiscalYear.DoesNotExist:
        return redirect('account_logout')

    selected_month = dict()

    for m in months:
        if m.get('id') == month:
            selected_month = m

    currency = Currency.objects.get(symbol=symbol)

    incomes_total = Income.objects.filter(currency=currency).all()
    outcomes_total = Outcome.objects.filter(currency=currency).all()

    outcomes_obj = Outcome.objects.filter(currency=currency, out_at__month=selected_month['id'],
                                          out_at__year=fiscal_year.year).all()

    total_checkout_income = incomes_total.aggregate(Sum('amount'))
    balance_income = 0

    total_checkout_outcome = outcomes_total.aggregate(Sum('amount'))
    balance_outcome = 0

    if total_checkout_income['amount__sum'] is not None:
        balance_income = total_checkout_income['amount__sum']

    if total_checkout_outcome['amount__sum'] is not None:
        balance_outcome = total_checkout_outcome['amount__sum']

    balance = balance_income - balance_outcome

    if request.method == 'POST':

        if request.POST.get('edit_record_id'):
            pk = request.POST['edit_record_id']
            outcome = Outcome.objects.get(id=pk)
            form = OutcomeModelForm(request.POST, instance=outcome)

            if form.is_valid():
                form.save()
                messages.success(request,
                                 'Dépense pour le compte [{}] du [{}] a été modifiée avec succès. Montant: [{}] [{}]'.format(
                                     outcome.accounting_additional, localize(outcome.out_at, use_l10n=True),
                                     outcome.amount,
                                     outcome.currency.symbol))
            path = resolve_url(request.path)
            return redirect(path)

        if request.POST.get('remove_record_id'):
            pk = request.POST['remove_record_id']
            outcome_data = Outcome.objects.get(id=pk)

            try:
                outcome_data.delete()
                messages.success(request,
                                 'Dépense pour le compte [{}] du [{}] / [{}]  a été supprimée avec succès. Montant: [{}] [{}]'.format(
                                     outcome_data.accounting_additional, localize(outcome_data.out_at, use_l10n=True),
                                     outcome_data.more, outcome_data.amount, outcome_data.currency.symbol))
                path = resolve_url(request.path)
                return redirect(path)
            except:
                pass

        form = OutcomeModelForm(request.POST)

        if form.is_valid():
            outcome = form.save(commit=False)

            if outcome.amount > balance:
                messages.error(request,
                               'Votre solde est insuffisant pour éffectuer cette opération! [{} {}]'.format(
                                   balance, currency.symbol))
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
                messages.success(request,
                                 'Dépense pour le compte [{}] a été enregistrée avec succès. Montant: [{}] [{}]'.format(
                                     outcome.accounting_additional, outcome.amount, outcome.currency.symbol))
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
        'current_checkout': 'images/flags/' + currency.country_code + '.svg',
        'selected_month': selected_month,
        'outcomes': outcomes_obj,
        'total_checkout': total_checkout_outcome,
        'balance': balance
    }
    return render(request, 'treasury/outcomes.html', context)


@login_required()
def accounting_additional(request):
    accounting_main_id = request.GET.get('accounting_main_id')
    accounting_main = Main.objects.get(id=accounting_main_id)
    accountings_additional = Additional.objects.filter(account_main=accounting_main).all()

    return JsonResponse(list(accountings_additional.values('id', 'account_name')), safe=False)


@login_required()
def accounting_adjunct(request):
    accounting_additional_id = request.GET.get('accounting_additional_id')
    accounting = Additional.objects.get(id=accounting_additional_id)
    accountings_adjunct = Adjunct.objects.filter(account_additional=accounting).all()

    return JsonResponse(list(accountings_adjunct.values('id', 'adjunct_account_name')), safe=False)


@login_required()
def accounting_monitoring(request):
    year_id = request.session.get('year')
    year = FiscalYear.objects.get(id=year_id)

    accounting_additional_id = request.GET.get('accounting_additional_id')
    accounting = Additional.objects.get(id=accounting_additional_id)

    monitor = Monitoring.objects.filter(accounting=accounting, year=year,
                                        accounting__account_main__account_type__contains='decaissement')

    return JsonResponse(list(monitor.values('id', 'warn_at', 'message')), safe=False)


@login_required()
def edit_income(request, pk):
    income = Income.objects.get(id=pk)
    income_serializer = IncomeSerializer(income, many=False)
    return JsonResponse(income_serializer.data, safe=False)


@login_required()
def edit_outcome(request, pk):
    outcome = Outcome.objects.get(id=pk)
    outcome_serializer = OutcomeSerializer(outcome, many=False)
    return JsonResponse(outcome_serializer.data, safe=False)


@permission_classes([IsAuthenticated])
def api_balance(request, symbol):
    year_id = request.session.get('year')
    try:
        fiscal_year = FiscalYear.objects.get(id=year_id)
    except FiscalYear.DoesNotExist:
        return redirect('account_logout')

    currency = Currency.objects.get(symbol=symbol)
    balances = list()
    for i in range(1, 13):

        incomes_total = Income.objects.filter(currency=currency, in_at__month=i, in_at__year=fiscal_year.year).all()
        outcomes_total = Outcome.objects.filter(currency=currency, out_at__month=i, out_at__year=fiscal_year.year).all()
        budget = Budget.objects.filter(plan_at__month=i, plan_at__year=fiscal_year.year)

        total_checkout_income = incomes_total.aggregate(Sum('amount'))
        balance_income = 0

        total_checkout_outcome = outcomes_total.aggregate(Sum('amount'))
        balance_outcome = 0

        budget_total = budget.aggregate(Sum('amount'))
        balance_budget = 0

        if total_checkout_income['amount__sum'] is not None:
            balance_income = total_checkout_income['amount__sum']

        if total_checkout_outcome['amount__sum'] is not None:
            balance_outcome = total_checkout_outcome['amount__sum']

        if budget_total['amount__sum'] is not None:
            balance_budget = budget_total['amount__sum']

        balances.append(
            {'month': i, 'year': fiscal_year.year, 'income': balance_income, 'outcome': balance_outcome,
             'budget': balance_budget, 'currency': currency.symbol})
    return JsonResponse(balances, safe=False)
