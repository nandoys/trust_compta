from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name="account_login"),
    path('logout/', views.logout_view, name="account_logout"),
    path('annee-exercice/', views.fiscal_year, name="fiscal_year"),
    path('paramètres/', views.settings, name="settings"),
]
