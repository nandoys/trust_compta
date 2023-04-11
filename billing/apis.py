from django.urls import path
from . import views

urlpatterns = [
    path('partners/get', views.api_get_partners, name="api_get_partners"),
    path('partner/save', views.api_save_partner, name="api_post_partner"),
    path('customer/bills/get', views.api_get_customer_bills, name="api_get_customer_bills"),
    path('customer/bill/<uuid:bill_id>/accounting/entries/get', views.api_get_customer_bill_accounting_entries,
         name="api_get_customer_bill_accounting_entries"),
]
