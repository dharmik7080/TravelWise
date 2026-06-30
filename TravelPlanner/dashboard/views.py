from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

class PredictionsView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/predictions.html'

