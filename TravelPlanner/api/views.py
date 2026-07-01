from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import PermissionDenied
from destinations.models import Destination
from attractions.models import Attraction
from packages.models import Package
from trips.models import Trip, ItineraryTemplate, ItineraryDay
from seasons.models import BestSeason
from .serializers import (
    DestinationSerializer,
    AttractionSerializer,
    PackageSerializer,
    TripSerializer,
    ItineraryTemplateSerializer,
    ItineraryDaySerializer,
    BestSeasonSerializer,
)
from .permissions import IsStaffOrReadOnly, IsTripOwner, IsItineraryDayOwner

class DestinationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Destination records. Accessible publicly read-only, edits restricted to staff users.
    """
    serializer_class = DestinationSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['destination_name', 'city', 'state', 'region', 'category', 'description']
    ordering_fields = ['destination_name', 'average_cost_per_day', 'average_rating', 'ideal_days']

    def get_queryset(self):
        queryset = Destination.objects.all().order_by('destination_name')

        # Custom filtering
        state = self.request.query_params.get('state')
        category = self.request.query_params.get('category')
        budget_level = self.request.query_params.get('budget_level')
        best_season = self.request.query_params.get('best_season')

        if state:
            queryset = queryset.filter(state__iexact=state.strip())
        if category:
            queryset = queryset.filter(category__iexact=category.strip())
        if budget_level:
            queryset = queryset.filter(budget_level__iexact=budget_level.strip())
        if best_season:
            queryset = queryset.filter(best_season__iexact=best_season.strip())

        return queryset


class AttractionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Attraction records. Publicly read-only, edits restricted to staff users.
    """
    serializer_class = AttractionSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['attraction_name', 'description', 'category']
    ordering_fields = ['attraction_name', 'entry_fee', 'visit_time']

    def get_queryset(self):
        queryset = Attraction.objects.select_related('destination').all().order_by('attraction_name')
        destination_id = self.request.query_params.get('destination')
        category = self.request.query_params.get('category')
        
        if destination_id:
            queryset = queryset.filter(destination_id=destination_id)
        if category:
            queryset = queryset.filter(category__iexact=category.strip())
            
        return queryset


class PackageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Package records. Publicly read-only, edits restricted to staff users.
    """
    serializer_class = PackageSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['package_name', 'description', 'package_type']
    ordering_fields = ['package_name', 'duration', 'price']

    def get_queryset(self):
        queryset = Package.objects.select_related('destination').all().order_by('package_name')
        destination_id = self.request.query_params.get('destination')
        package_type = self.request.query_params.get('package_type')
        
        if destination_id:
            queryset = queryset.filter(destination_id=destination_id)
        if package_type:
            queryset = queryset.filter(package_type__iexact=package_type.strip())
            
        return queryset


class ItineraryTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ItineraryTemplate records. Publicly read-only, edits restricted to staff users.
    """
    serializer_class = ItineraryTemplateSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        queryset = ItineraryTemplate.objects.select_related('destination').all().order_by('destination', 'day_number')
        destination_id = self.request.query_params.get('destination')
        if destination_id:
            queryset = queryset.filter(destination_id=destination_id)
        return queryset


class TripViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Trip records. Requires authentication, restricts access/visibility to owner.
    """
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated, IsTripOwner]

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Trip.objects.none()
        return Trip.objects.select_related('destination', 'user').filter(user=self.request.user).order_by('-start_date')

    def perform_create(self, serializer):
        # Automatically assign the logged-in user as the trip owner
        trip = serializer.save(user=self.request.user)

        # Automatically generate day-by-day ItineraryDays upon Trip creation via API
        days = (trip.end_date - trip.start_date).days + 1
        templates = list(ItineraryTemplate.objects.filter(destination=trip.destination).order_by('day_number'))

        for i in range(1, days + 1):
            if templates:
                template = templates[(i - 1) % len(templates)]
                morning = template.morning
                afternoon = template.afternoon
                evening = template.evening
            else:
                morning = "Explore local spots and landmarks"
                afternoon = "Enjoy local cuisine and markets"
                evening = "Relax and experience the nightlife"

            ItineraryDay.objects.create(
                trip=trip,
                day_number=i,
                morning=morning,
                afternoon=afternoon,
                evening=evening
            )


class ItineraryDayViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ItineraryDay records. Requires authentication, restricts access/visibility to owner.
    """
    serializer_class = ItineraryDaySerializer
    permission_classes = [permissions.IsAuthenticated, IsItineraryDayOwner]

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return ItineraryDay.objects.none()
        return ItineraryDay.objects.select_related(
            'trip', 'trip__destination', 'trip__user'
        ).filter(trip__user=self.request.user).order_by('trip', 'day_number')

    def perform_create(self, serializer):
        # Ensure the user owns the trip they are adding an itinerary day to
        trip = serializer.validated_data.get('trip')
        if trip.user != self.request.user:
            raise PermissionDenied("You do not own this trip.")
        serializer.save()

    def perform_update(self, serializer):
        trip = serializer.instance.trip
        if trip.user != self.request.user:
            raise PermissionDenied("You do not own this trip.")
        serializer.save()


class BestSeasonViewSet(viewsets.ModelViewSet):
    """
    ViewSet for BestSeason records. Publicly read-only, edits restricted to staff users.
    """
    serializer_class = BestSeasonSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['season', 'peak_months', 'average_temperature', 'rainfall', 'travel_tip']
    ordering_fields = ['season', 'average_temperature']

    def get_queryset(self):
        queryset = BestSeason.objects.select_related('destination').all().order_by('destination', 'season')
        destination_id = self.request.query_params.get('destination')
        if destination_id:
            queryset = queryset.filter(destination_id=destination_id)
        return queryset


from django.views.generic import TemplateView

class ApiDocsView(TemplateView):
    """
    Saves and renders static API documentation using Bootstrap 5.
    """
    template_name = 'api/docs.html'
