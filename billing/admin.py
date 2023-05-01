from django.contrib import admin

from .models import CustomerBill, SupplierBill, BillLine, BillLineTax, Partner

# Register your models here.
admin.site.register([CustomerBill, SupplierBill, BillLine, BillLineTax, Partner])
