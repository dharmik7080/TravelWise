from django.contrib import admin
from django.utils.html import format_html
from .models import Attraction

@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    """
    Admin configuration for Attraction database records.
    """
    list_display = ('image_preview', 'attraction_name', 'destination', 'category', 'entry_fee', 'opening_time', 'closing_time')
    list_filter = ('destination', 'category')
    search_fields = ('attraction_name', 'destination__destination_name')
    ordering = ('destination', 'attraction_name')
    raw_id_fields = ('destination',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 4px;" />', obj.image.url)
        return format_html('<span style="color: #999;">No Image</span>')

    image_preview.short_description = 'Preview'
