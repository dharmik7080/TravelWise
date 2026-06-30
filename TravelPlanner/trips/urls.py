from django.urls import path
from .views import (
    TripsIndexView, TripCreateView, TripDetailView,
    TripUpdateView, TripDeleteView, TripItineraryUpdateView
)

app_name = 'trips'

urlpatterns = [
    path('', TripsIndexView.as_view(), name='index'),
    path('plan/', TripCreateView.as_view(), name='plan'),
    path('<int:pk>/', TripDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', TripUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', TripDeleteView.as_view(), name='delete'),
    path('<int:pk>/itinerary/edit/', TripItineraryUpdateView.as_view(), name='edit_itinerary'),
]
