import uuid
from django.db import models

from accounting_plan.models import Main, Additional, Adjunct


# Create your models here.

class Currency(models.Model):
    countries_iso = [('us', 'us'), ('cd', 'cd'), ('eur', 'eur')]
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255, unique=True)
    symbol_iso = models.CharField(max_length=3, unique=True)
    country_iso = models.CharField(max_length=3, unique=True, choices=countries_iso)
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


class Outcome(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)
    accounting_main = models.ForeignKey(Main, on_delete=models.CASCADE)
    accounting_additional = models.ForeignKey(Additional, on_delete=models.CASCADE)
    accounting_adjunct = models.ForeignKey(Adjunct, on_delete=models.SET_NULL, null=True)
    slip_number = models.CharField(max_length=255)
    amount = models.FloatField()
    out_at = models.DateField()
    write_at = models.DateTimeField(auto_now=True)
    more = models.CharField(max_length=255, null=True)
    daily_rate = models.ForeignKey(CurrencyDailyRate, on_delete=models.SET_NULL, null=True)


class Income(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)
    accounting_main = models.ForeignKey(Main, on_delete=models.CASCADE)
    accounting_additional = models.ForeignKey(Additional, on_delete=models.CASCADE, null=True)
    accounting_adjunct = models.ForeignKey(Adjunct, on_delete=models.SET_NULL, null=True)
    slip_number = models.CharField(max_length=255, null=True)
    amount = models.FloatField()
    in_at = models.DateField()
    write_at = models.DateTimeField(auto_now=True)
    more = models.CharField(max_length=255, null=True)
    daily_rate = models.ForeignKey(CurrencyDailyRate, on_delete=models.SET_NULL, null=True)

