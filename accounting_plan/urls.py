from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="accounting_plan_index"),
    path('compte/<uuid:pk>', views.accounting_main_details, name="accounting_main_details"),
    path('compte/sous-compte/<uuid:pk>/<int:fy>', views.accounting_budget, name="accounting_budget"),
    path('comptes/<str:account_type>', views.api_get_accounting_main_by_type, name="api_get_accounting_main_by_type")
]