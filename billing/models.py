import uuid
from django.db import models

from accounting.models import Document


class Partner(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    street = models.CharField(max_length=255, null=True)
    town = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255, null=True)
    telephone = models.CharField(max_length=255, null=True)


class CustomerBill(Document):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    bill_at = models.DateField()
    deadline_at = models.DateField()
    currency = models.ForeignKey('treasury.Currency', on_delete=models.SET_NULL, null=True)
    amount = models.FloatField(null=True, blank=True)
    amount_foreign = models.FloatField(null=True, blank=True)
    rate = models.IntegerField(default=1)
    is_lettered = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)


class SupplierBill(Document):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    paying_reference = models.CharField(max_length=255, null=True)
    bank_account_number = models.CharField(max_length=255, null=True)
    bill_at = models.DateField()
    accounting_date = models.DateField()
    deadline_at = models.DateField()
    currency = models.ForeignKey('treasury.Currency', on_delete=models.SET_NULL, null=True)
    amount = models.FloatField()
    amount_foreign = models.FloatField(null=True)
    rate = models.IntegerField(default=1)
    is_lettered = models.BooleanField(default=False)


class BillLine(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    customer_bill = models.ForeignKey('CustomerBill', on_delete=models.CASCADE, null=True, blank=True)
    supplier_bill = models.ForeignKey('SupplierBill', on_delete=models.CASCADE, null=True, blank=True)
    label = models.CharField(max_length=255, null=True)
    account = models.ForeignKey('accounting.Plan', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    price_with_tax = models.FloatField()


class BillLineTax(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    tax = models.ForeignKey('accounting.Tax', on_delete=models.CASCADE)
    tax_amount = models.FloatField()
    bill_line = models.ForeignKey('BillLine', on_delete=models.CASCADE, related_name='bill_line_tax')


class CustomerBillPayment(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    reference = models.CharField(max_length=255)
    account = models.ForeignKey('accounting.Plan', on_delete=models.SET_NULL, null=True)
    ref_bill = models.ForeignKey('billing.CustomerBill', on_delete=models.CASCADE)
    paid_at = models.DateField()
    amount = models.FloatField()
    amount_foreign = models.FloatField(null=True)
    rate = models.IntegerField(default=1)
    currency = models.ForeignKey('treasury.Currency', on_delete=models.SET_NULL, null=True)


class SupplierBillPayment(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    reference = models.CharField(max_length=255)
    account = models.ForeignKey('accounting.Plan', on_delete=models.SET_NULL, null=True)
    ref_bill = models.ForeignKey('billing.SupplierBill', on_delete=models.CASCADE)
    paid_at = models.DateField()
    amount = models.FloatField()
    amount_foreign = models.FloatField(null=True)
    rate = models.IntegerField(default=1)
    currency = models.ForeignKey('treasury.Currency', on_delete=models.SET_NULL, null=True)
