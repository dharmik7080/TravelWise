from django.contrib import admin
from .models import Trip, ItineraryTemplate, ItineraryDay

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    """
    Admin configuration for traveler planned Trips.
    """
    list_display = ('destination', 'user', 'start_date', 'end_date', 'number_of_travelers', 'budget', 'travel_type')
    list_filter = ('travel_type',)
    search_fields = ('user__username', 'destination__destination_name')
    ordering = ('start_date',)
    raw_id_fields = ('destination', 'user')


@admin.register(ItineraryTemplate)
class ItineraryTemplateAdmin(admin.ModelAdmin):
    """
    Admin settings configuration for predefined day itinerary templates.
    """
    list_display = ('destination', 'day_number', 'morning', 'afternoon', 'evening')
    list_filter = ('destination',)
    search_fields = ('destination__destination_name', 'morning', 'afternoon', 'evening')
    ordering = ('destination', 'day_number')
    raw_id_fields = ('destination',)


@admin.register(ItineraryDay)
class ItineraryDayAdmin(admin.ModelAdmin):
    """
    Admin settings configuration for actual day-by-day travel trip itineraries.
    """
    list_display = ('trip', 'day_number', 'morning', 'afternoon', 'evening')
    list_filter = ('trip__destination', 'trip__user')
    search_fields = ('trip__destination__destination_name', 'trip__user__username', 'morning', 'afternoon', 'evening')
    ordering = ('trip', 'day_number')
    raw_id_fields = ('trip',)
