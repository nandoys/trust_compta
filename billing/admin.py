from django.contrib import admin

from .models import CustomerBill, SupplierBill, BillLine, Partner

# Register your models here.
admin.site.register([CustomerBill, SupplierBill, BillLine, Partner])
