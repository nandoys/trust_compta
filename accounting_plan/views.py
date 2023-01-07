import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Main, Additional, FiscalYear, Budget
from .forms import MainAccountingForm, AdditionalAccountingForm, AdjunctAccountingForm, BudgetAccountingForm, \
    FiscalYearForm
from .serializer import MainSerializer


# Create your views here.

def index(request):
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
    form = MainAccountingForm()
    context = {
        'main_accountings': main_accountings,
        'form': form
    }
    return render(request, 'accounting_plan/index.html', context)


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
            'form': form
        }
        return render(request, 'accounting_plan/main_accounting_details.html', context)
    except Main.DoesNotExist:
        return redirect('accounting_plan_index')


def accounting_budget(request, pk, fy):
    try:
        fiscal_years = FiscalYear.objects.all()
        fiscal_year = FiscalYear.objects.get(year=fy)
        additional_accounting = Additional.objects.get(id=pk)
        budgets = Budget.objects.filter(accounting=additional_accounting, fiscal_year=fiscal_year)

        total_budget = budgets.aggregate(Sum('amount'))

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
                        budget.fiscal_year = fiscal_year
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
