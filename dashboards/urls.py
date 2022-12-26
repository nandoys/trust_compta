from django.urls import path
from dashboards.views import (
    dashboard_view
)

app_name = 'dashboards'

urlpatterns = [
    path('',view =dashboard_view,name="dashboard"),

]
