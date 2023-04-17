import uuid
from django.db import models
from django.contrib.auth.models import User

from accounting.models import Document
from billing.models import Partner


class Currency(models.Model):
    countries__code = [('us', 'us'), ('cd', 'cd'), ('eur', 'eur')]
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255, unique=True)
    symbol = models.CharField(max_length=10, unique=True)
    country_code = models.CharField(max_length=3, unique=True, choices=countries__code)
    is_local = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CurrencyDailyRate(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    from_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='from_currency')
    to_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='to_currency')
    rate = models.IntegerField()
    rate_at = models.DateField(auto_now=True, unique=True)
    in_use = models.BooleanField(default=True)

    def __str__(self):
        return "Taux du " + self.rate_at.__str__()

    class Meta:
        db_table = 'currency_daily_rate'


class CurrencyDiffrenceRate(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    account = models.ForeignKey('accounting.Plan', on_delete=models.CASCADE, related_name='account_currency_difference_rate')
    diff_category = models.ForeignKey('accounting.PlanCategory', on_delete=models.CASCADE, related_name='currency_difference_category')


class Outcome(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)
    accounting_main = models.ForeignKey('accounting.Main', on_delete=models.CASCADE)
    accounting_additional = models.ForeignKey('accounting.Additional', on_delete=models.CASCADE, null=True, blank=True)
    accounting_adjunct = models.ForeignKey('accounting.Adjunct', on_delete=models.SET_NULL, null=True, blank=True)
    slip_number = models.CharField(max_length=255)
    amount = models.FloatField()
    out_at = models.DateField()
    write_at = models.DateTimeField(auto_now=True)
    more = models.CharField(max_length=255, null=True, blank=True)
    daily_rate = models.ForeignKey(CurrencyDailyRate, on_delete=models.SET_NULL, null=True, blank=True)


class Income(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)
    accounting_main = models.ForeignKey('accounting.Main', on_delete=models.CASCADE)
    accounting_additional = models.ForeignKey('accounting.Additional', on_delete=models.SET_NULL, null=True, blank=True)
    accounting_adjunct = models.ForeignKey('accounting.Adjunct', on_delete=models.SET_NULL, null=True, blank=True)
    slip_number = models.CharField(max_length=255, null=True)
    amount = models.FloatField()
    in_at = models.DateField()
    write_at = models.DateTimeField(auto_now=True)
    more = models.CharField(max_length=255, null=True, blank=True)
    daily_rate = models.ForeignKey(CurrencyDailyRate, on_delete=models.SET_NULL, null=True)


class AccountingEntry(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    account = models.ForeignKey('accounting.Plan', on_delete=models.CASCADE, related_name='account_entry')
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE, related_name='currency_entry')
    rate = models.IntegerField(default=1)
    ref_statement = models.ForeignKey('Statement', on_delete=models.CASCADE, null=True, blank=True, related_name='ref_statement_entry')
    ref_billing_customer = models.ForeignKey('billing.CustomerBill', on_delete=models.CASCADE, null=True, blank=True,
                                             related_name='ref_billing_customer_entry')
    ref_billing_supplier = models.ForeignKey('billing.SupplierBill', on_delete=models.CASCADE, null=True, blank=True,
                                             related_name='ref_billing_supplier_entry')
    ref_bill_line = models.ForeignKey('billing.BillLine', on_delete=models.CASCADE, null=True, related_name='ref_bill_line_entry')
    label = models.CharField(max_length=255, null=True, blank=True)
    partner = models.ForeignKey(Partner, on_delete=models.SET_NULL, null=True, blank=True, related_name='partner_entry')
    date_at = models.DateField()
    amount_foreign = models.FloatField(blank=True, null=True)
    debit = models.FloatField(blank=True, null=True)
    credit = models.FloatField(blank=True, null=True)
    write_at = models.DateTimeField(auto_now=True)
    done_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_verified = models.BooleanField(default=False)

    @classmethod
    def has_counter_party(cls, reference_id: uuid.UUID, reference_type):
        if reference_type == 'statement':
            count = cls.objects.filter(ref_statement__id=reference_id).count()
            if count >= 1:
                return True
            else:
                return False
        elif reference_type == 'customer':
            count = cls.objects.filter(ref_billing_customer__id=reference_id).count()
            if count > 1:
                return True
            else:
                return count
        elif reference_type == 'supplier':
            count = cls.objects.filter(ref_billing_supplier_id=reference_id).count()
            if count > 1:
                return True
            else:
                return False
        else:
            return None

    class Meta:
        db_table = 'accounting_entry'
        verbose_name_plural = 'Accounting_entries'


class Statement(Document):
    transaction_at = models.DateField()
    amount = models.FloatField()
    currency = models.ForeignKey('treasury.Currency', on_delete=models.SET_NULL, null=True)
    rate = models.IntegerField()
