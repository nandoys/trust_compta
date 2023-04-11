from django.urls import path
from . import views

urlpatterns = [
    path('incomes/get', views.api_get_incomes, name="api_get_incomes"),
    path('statement/save', views.api_save_statement, name="api_save_statement"),
    path('statements/get', views.api_get_statements, name="api_get_statements"),
    path('currencies/get', views.api_get_currencies, name="api_get_currencies"),
]
