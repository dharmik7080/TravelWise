from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DestinationViewSet,
    AttractionViewSet,
    PackageViewSet,
    ItineraryTemplateViewSet,
    TripViewSet,
    ItineraryDayViewSet,
    ApiDocsView,
    BestSeasonViewSet,
)

router = DefaultRouter()
router.register(r'destinations', DestinationViewSet, basename='destination')
router.register(r'attractions', AttractionViewSet, basename='attraction')
router.register(r'packages', PackageViewSet, basename='package')
router.register(r'itinerary-templates', ItineraryTemplateViewSet, basename='itinerary-template')
router.register(r'trips', TripViewSet, basename='trip')
router.register(r'itinerary-days', ItineraryDayViewSet, basename='itinerary-day')
router.register(r'seasons', BestSeasonViewSet, basename='season')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('docs/', ApiDocsView.as_view(), name='api-docs'),
]
