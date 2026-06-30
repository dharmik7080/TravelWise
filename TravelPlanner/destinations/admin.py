from django.contrib import admin
from django.utils.html import format_html
from .models import Destination

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'destination_name', 'city', 'state', 'category', 'budget_level', 'average_rating')
    list_filter = ('state', 'category', 'budget_level', 'family_friendly', 'couple_friendly', 'solo_friendly')
    search_fields = ('destination_name', 'city', 'state')
    ordering = ('-average_rating',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 4px;" />', obj.image.url)
        return format_html('<span style="color: #999;">No Image</span>')
    
    image_preview.short_description = 'Preview'
