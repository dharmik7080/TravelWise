from django.urls import path
from .views import DashboardIndexView, PredictionsView

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardIndexView.as_view(), name='index'),
    path('predictions/', PredictionsView.as_view(), name='predictions'),
]
