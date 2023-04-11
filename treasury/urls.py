from django.urls import path
from . import views

urlpatterns = [
    path('tableau-de-bord', views.index, name="treasury_index"),
    path('caisse/<str:module_id>/<str:symbol>/<int:month>/<int:year>', views.checkout, name="treasury_checkout"),
    path('<str:symbol>/depenses/<int:month>', views.outcomes, name="treasury_outcomes"),
    path('additioinal/tags', views.accounting_additional, name="accounting_additional_input"),
    path('adjunct/tags', views.accounting_adjunct, name="accounting_adjunct_input"),
    path('monitoring/', views.accounting_monitoring, name="accounting_monitoring"),
    path('income/<uuid:pk>', views.edit_income, name="edit_income"),
    path('outcome/<uuid:pk>', views.edit_outcome, name="edit_outcome"),
    path('balance/<str:symbol>', views.api_balance, name="api_balance")
]
