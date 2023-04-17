from django.urls import path

from . import views

urlpatterns = [
    path('journal', views.api_get_journal, name='api_get_journal')
]