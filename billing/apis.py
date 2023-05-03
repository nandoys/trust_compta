from django.urls import path
from . import views

urlpatterns = [
    path('partners/get', views.api_get_partners, name="api_get_partners"),
    path('partner/save', views.api_save_partner, name="api_post_partner"),
    path('customer/bill/save', views.api_save_bill, name="api_save_bill"),
    path('customer/bill/update', views.api_update_bill, name="api_update_bill"),
    path('customer/bill/entries/save', views.api_save_customer_bill_entry, name="api_save_customer_bill"),
    path('customer/bill/entries/delete', views.api_delete_customer_bill_entry, name="api_delete_customer_bill"),
    path('customer/bills/get', views.api_get_customer_bills, name="api_get_customer_bills"),
    path('customer/bill/lines/get', views.api_get_customer_bill_lines, name="api_get_customer_bill_lines"),
    path('customer/bill/<uuid:bill_id>/accounting/entries/get', views.api_get_customer_bill_accounting_entries,
         name="api_get_customer_bill_accounting_entries"),
]
