from django.contrib import admin
from django.utils.html import format_html
from .models import Package

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    """
    Admin settings configuration for Package records.
    """
    list_display = ('image_preview', 'package_name', 'destination', 'duration', 'package_type', 'price')
    list_filter = ('destination', 'package_type')
    search_fields = ('package_name', 'destination__destination_name')
    ordering = ('destination', '-price')
    raw_id_fields = ('destination',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 4px;" />', obj.image.url)
        return format_html('<span style="color: #999;">No Image</span>')

    image_preview.short_description = 'Preview'
