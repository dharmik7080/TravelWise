from django.contrib import admin
from django.utils.html import format_html
from .models import Destination

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    """
    Enhanced Admin interface for the Destination model.
    """
    list_display = ('image_preview', 'destination_name', 'state', 'category', 'budget_level', 'best_season', 'average_rating')
    list_filter = ('state', 'category', 'budget_level')
    search_fields = ('destination_name', 'city')
    ordering = ('destination_name',)
    list_per_page = 20
    change_list_template = "admin/custom_change_list.html"

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('export-csv/', self.admin_site.admin_view(self.export_csv_view), name='destinations_destination_export_csv'),
        ]
        return custom_urls + urls

    def export_csv_view(self, request):
        from destinations.admin_utils import export_queryset_to_csv
        fields = [
            'destination_name', 'city', 'state', 'region', 'category', 
            'description', 'best_season', 'ideal_days', 'budget_level', 
            'average_cost_per_day', 'family_friendly', 'couple_friendly', 
            'solo_friendly', 'average_rating'
        ]
        queryset = self.get_queryset(request)
        return export_queryset_to_csv(queryset, fields, "destinations.csv")

    readonly_fields = ('image_preview_form',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('destination_name', 'city', 'state', 'region', 'category', 'description')
        }),
        ('Travel Details & Suitability', {
            'fields': ('best_season', 'ideal_days', 'family_friendly', 'couple_friendly', 'solo_friendly')
        }),
        ('Pricing & Ratings', {
            'fields': ('budget_level', 'average_cost_per_day', 'average_rating')
        }),
        ('Destination Image', {
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
