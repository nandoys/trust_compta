from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="treasury_index"),
    path('revenus', views.incomes, name="treasury_incomes"),
    path('<str:symbol>/depenses/<int:year>', views.outcomes, name="treasury_outcomes"),
    path('tags', views.tags, name="tags_input")
]