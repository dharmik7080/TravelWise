from django.contrib import admin
from django.utils import timezone
from .models import Trip, ItineraryTemplate, ItineraryDay

class TripStatusListFilter(admin.SimpleListFilter):
    """
    Custom list filter to sort Trips by upcoming or completed status.
    """
    title = 'Trip Status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('upcoming', 'Upcoming'),
            ('completed', 'Completed'),
        )

    def queryset(self, request, queryset):
        current_date = timezone.localtime(timezone.now()).date()
        if self.value() == 'upcoming':
            return queryset.filter(start_date__gte=current_date)
        elif self.value() == 'completed':
            return queryset.filter(end_date__lt=current_date)
        return queryset

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    """
    Admin configuration for traveler planned Trips.
    """
    list_display = ('get_username', 'destination', 'start_date', 'end_date', 'budget', 'travel_type')
    list_filter = ('travel_type', TripStatusListFilter)
    search_fields = ('user__username', 'destination__destination_name')
    ordering = ('start_date',)
    raw_id_fields = ('destination', 'user')
    change_list_template = "admin/custom_change_list.html"

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('export-csv/', self.admin_site.admin_view(self.export_csv_view), name='trips_trip_export_csv'),
        ]
        return custom_urls + urls

    def export_csv_view(self, request):
        from destinations.admin_utils import export_queryset_to_csv
        fields = [
            'user__username', 'destination__destination_name', 'start_date', 
            'end_date', 'number_of_travelers', 'budget', 'travel_type'
        ]
        queryset = self.get_queryset(request)
        return export_queryset_to_csv(queryset, fields, "trips.csv")

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'
    get_username.admin_order_field = 'user__username'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'destination')


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
