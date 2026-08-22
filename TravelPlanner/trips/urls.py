from django.urls import path
from .views import (
    TripsIndexView, TripCreateView, TripDetailView,
    TripUpdateView, TripDeleteView, TripItineraryUpdateView,
    TripCostEstimateView, TripItineraryGenerateView,
    TripCalendarView, TripShareToggleView, TripPublicView,
    TripCopyView, TripBudgetView
)

app_name = 'trips'

urlpatterns = [
    path('', TripsIndexView.as_view(), name='index'),
    path('plan/', TripCreateView.as_view(), name='plan'),
    path('calendar/', TripCalendarView.as_view(), name='calendar'),
    path('estimate-cost/', TripCostEstimateView.as_view(), name='estimate_cost'),
    path('generate-itinerary/', TripItineraryGenerateView.as_view(), name='generate_itinerary'),
    path('shared/<uuid:share_token>/', TripPublicView.as_view(), name='public'),
    path('shared/<uuid:share_token>/copy/', TripCopyView.as_view(), name='copy_trip'),
    path('<int:pk>/', TripDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', TripUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', TripDeleteView.as_view(), name='delete'),
    path('<int:pk>/budget/', TripBudgetView.as_view(), name='budget'),
    path('<int:pk>/itinerary/edit/', TripItineraryUpdateView.as_view(), name='edit_itinerary'),
    path('<int:pk>/share/toggle/', TripShareToggleView.as_view(), name='share_toggle'),
]
