from django.contrib import admin
from .models import BestSeason

@admin.register(BestSeason)
class BestSeasonAdmin(admin.ModelAdmin):
    """
    Admin configuration for BestSeason records.
    """
    list_display = ('destination', 'season', 'peak_months', 'average_temperature', 'rainfall')
    list_filter = ('destination', 'season')
    search_fields = ('season', 'destination__destination_name')
    ordering = ('destination', 'season')
    raw_id_fields = ('destination',)
