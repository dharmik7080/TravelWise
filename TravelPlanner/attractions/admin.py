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
    search_fields = ('attraction_name', 'destination__destination_name', 'category')
    ordering = ('attraction_name',)
    raw_id_fields = ('destination',)
    list_per_page = 20

    readonly_fields = ('image_preview_form',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('attraction_name', 'destination', 'category', 'description')
        }),
        ('Timing & Costs', {
            'fields': ('opening_time', 'closing_time', 'average_visit_time', 'entry_fee')
        }),
        ('Media Assets', {
            'fields': ('image', 'image_preview_form')
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 4px; object-fit: cover;" />', obj.image.url)
        return format_html('<span style="color: #6c757d; font-size: 0.85rem;">No Image</span>')
    image_preview.short_description = 'Image'

    def image_preview_form(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 300px; border-radius: 8px; object-fit: cover;" />', obj.image.url)
        return "No image uploaded yet."
    image_preview_form.short_description = 'Current Image Preview'
