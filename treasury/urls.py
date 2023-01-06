from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="treasury_index"),
    path('<str:symbol>/revenus/', views.incomes, name="treasury_incomes"),
    path('<str:symbol>/depenses/', views.outcomes, name="treasury_outcomes"),
    path('additioinal/tags', views.accounting_additional, name="accounting_additional_input"),
    path('adjunct/tags', views.accounting_adjunct, name="accounting_adjunct_input")
]