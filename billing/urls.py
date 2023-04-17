from django.urls import path

from . import views
urlpatterns = [
    path('customer', views.customers, name="customers"),
    path('suppliers', views.suppliers, name="suppliers"),
]