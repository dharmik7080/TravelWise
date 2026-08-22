from django.urls import path
from .views import DashboardIndexView, PredictionsView, AdminDashboardView

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardIndexView.as_view(), name='index'),
    path('predictions/', PredictionsView.as_view(), name='predictions'),
    path('admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
]
