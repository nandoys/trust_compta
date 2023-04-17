from django.urls import path
from . import views

urlpatterns = [

    path('plan/accounts-by-categories/get', views.api_get_accounts_by_category, name="api_get_accounts_by_category"),
    path('journal/<uuid:account_id>/get', views.api_get_accounts, name="api_get_accounts"),
    path('taxes/get', views.api_get_taxes, name="api_get_taxes")
]