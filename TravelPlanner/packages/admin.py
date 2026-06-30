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
    ordering = ('price',)
    raw_id_fields = ('destination',)
    list_per_page = 20
    change_list_template = "admin/custom_change_list.html"

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('export-csv/', self.admin_site.admin_view(self.export_csv_view), name='packages_package_export_csv'),
        ]
        return custom_urls + urls

    def export_csv_view(self, request):
        from destinations.admin_utils import export_queryset_to_csv
        fields = [
            'package_name', 'destination__destination_name', 'duration', 
            'package_type', 'price', 'description'
        ]
        queryset = self.get_queryset(request)
        return export_queryset_to_csv(queryset, fields, "packages.csv")

    readonly_fields = ('image_preview_form',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('package_name', 'destination', 'package_type', 'description')
        }),
        ('Duration & Pricing', {
            'fields': ('duration', 'price')
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
