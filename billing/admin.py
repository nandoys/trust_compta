from django.contrib import admin

from .models import CustomerBill, SupplierBill, BillEntry, Partner

# Register your models here.
admin.site.register([CustomerBill, SupplierBill, BillEntry, Partner])
