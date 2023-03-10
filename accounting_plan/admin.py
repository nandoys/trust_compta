from django.contrib import admin
from .models import Main, Additional, Adjunct, Budget, FiscalYear, Monitoring

# Register your models here.

admin.site.register([Main, Additional, Adjunct, Budget, FiscalYear, Monitoring])
