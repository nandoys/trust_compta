from django.contrib import admin

# Register your models here.
from .models import Journal, JournalType


admin.site.register([Journal, JournalType])
