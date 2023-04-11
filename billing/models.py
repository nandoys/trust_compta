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
    entry = models.ManyToManyField('BillEntry', related_name='customer_bill_entry')
    amount = models.FloatField()
    amount_foreign_currency = models.FloatField(null=True)
    rate = models.IntegerField(default=1)
    is_lettered = models.BooleanField(default=False)


class SupplierBill(Document):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    paying_reference = models.CharField(max_length=255, null=True)
    bank_account_number = models.CharField(max_length=255, null=True)
    bill_at = models.DateField()
    accounting_date = models.DateField()
    deadline_at = models.DateField()
    currency = models.ForeignKey('treasury.Currency', on_delete=models.SET_NULL, null=True)
    entry = models.ManyToManyField('BillEntry', related_name='supplier_bill_entry')
    amount = models.FloatField()
    amount_foreign_currency = models.FloatField(null=True)
    rate = models.IntegerField(default=1)
    is_lettered = models.BooleanField(default=False)


class BillEntry(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    label = models.CharField(max_length=255, null=True)
    account = models.ForeignKey('accounting.Plan', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    tax = models.ForeignKey('accounting.Tax', on_delete=models.SET_NULL, null=True)


class CustomerBillPayment(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    reference = models.CharField(max_length=255)
    account = models.ForeignKey('accounting.Plan', on_delete=models.SET_NULL, null=True)
    ref_bill = models.ForeignKey('billing.CustomerBill', on_delete=models.CASCADE)
    paid_at = models.DateField()
    amount = models.FloatField()
    amount_foreign_currency = models.FloatField(null=True)
    rate = models.IntegerField(default=1)
    currency = models.ForeignKey('treasury.Currency', on_delete=models.SET_NULL, null=True)


class SupplierBillPayment(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    reference = models.CharField(max_length=255)
    account = models.ForeignKey('accounting.Plan', on_delete=models.SET_NULL, null=True)
    ref_bill = models.ForeignKey('billing.SupplierBill', on_delete=models.CASCADE)
    paid_at = models.DateField()
    amount = models.FloatField()
    amount_foreign_currency = models.FloatField(null=True)
    rate = models.IntegerField(default=1)
    currency = models.ForeignKey('treasury.Currency', on_delete=models.SET_NULL, null=True)
