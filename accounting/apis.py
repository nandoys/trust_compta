from django.urls import path
from . import views

urlpatterns = [
    path('plan/main/get', views.api_get_main_account, name="api_get_main_account"),
    path('plan/main/debit/get', views.api_get_main_account_debit, name="api_get_main_account_debit"),
    path('plan/main/save', views.api_save_main_account, name="api_save_main_account"),
    path('plan/main/update', views.api_update_main_account, name="api_update_main_account"),
    path('plan/main/delete', views.api_delete_main_account, name="api_delete_main_account"),
    path('plan/main/<uuid:account_id>/subaccounts', views.api_get_subaccount_filter_main, name="api_get_subaccount_filter_main"),
    path('plan/main/<uuid:account_id>/debit/subaccounts', views.api_get_subaccount_debit_filter_main,
         name="api_get_subaccount_debit_filter_main"),
    path('plan/accounts-by-categories/get', views.api_get_accounts_by_category, name="api_get_accounts_by_category"),
    path('journal/<uuid:account_id>/get', views.api_get_accounts, name="api_get_accounts"),
]