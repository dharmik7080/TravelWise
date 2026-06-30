from django.urls import path
from .views import (
    DestinationListView, DestinationDetailView, DestinationCreateView,
    DestinationUpdateView, DestinationDeleteView
)

app_name = 'destinations'

urlpatterns = [
    path('', DestinationListView.as_view(), name='list'),
    path('add/', DestinationCreateView.as_view(), name='create'),
    path('<int:pk>/', DestinationDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', DestinationUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', DestinationDeleteView.as_view(), name='delete'),
]
