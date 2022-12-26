from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class DashboardView(LoginRequiredMixin,TemplateView):
    pass
    
dashboard_view = DashboardView.as_view(template_name="dashboards/index.html")




