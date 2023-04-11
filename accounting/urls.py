from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="accounting_index"),
    path('plan-comptable/', views.accounting_plan, name="accounting_plan"),
    path('compte/<uuid:pk>', views.accounting_main_details, name="accounting_main_details"),
    path('budget/', views.accounting_budget, name="accounting_budget"),
    path('budget/<uuid:pk>', views.budget_usage, name="budget_usage"),
    path('comptes/<str:account_type>', views.api_get_accounting_main_by_type, name="api_get_accounting_main_by_type"),
    path('reporting/<str:symbol>/', views.overall, name="accounting_reporting"),
    path('reporting/print', views.print_report, name="print_report")
]
