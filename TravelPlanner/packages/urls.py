from django.urls import path
from .views import (
    PackageListView, PackageDetailView, PackageCreateView,
    PackageUpdateView, PackageDeleteView
)

app_name = 'packages'

urlpatterns = [
    path('', PackageListView.as_view(), name='list'),
    path('add/', PackageCreateView.as_view(), name='create'),
    path('<int:pk>/', PackageDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', PackageUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', PackageDeleteView.as_view(), name='delete'),
]
