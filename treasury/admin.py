from django.contrib import admin

from .models import Currency, CurrencyDailyRate, Outcome

# Register your models here.

admin.site.register([Currency, CurrencyDailyRate, Outcome])
