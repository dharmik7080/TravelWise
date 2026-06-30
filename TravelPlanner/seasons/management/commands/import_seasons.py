import pandas as pd
from seasons.models import BestSeason
from destinations.models import Destination
from destinations.management.commands.base_import import BaseCSVImportCommand

class Command(BaseCSVImportCommand):
    help = 'Import best seasons from a CSV file using pandas'
    required_fields = [
        'destination_name', 'season', 'peak_months', 
        'average_temperature', 'rainfall', 'travel_tip'
    ]
    model_class = BestSeason
    import_type_name = "best seasons"

    def process_row(self, row, row_num):
        dest_name = str(row['destination_name']).strip()

        # Retrieve destination reference by name lookup
        try:
            destination = Destination.objects.get(destination_name__iexact=dest_name)
        except Destination.DoesNotExist:
            raise ValueError(f"Destination '{dest_name}' does not exist in database.")

        season = str(row['season']).strip()
        peak_months = str(row['peak_months']).strip()
        average_temperature = str(row['average_temperature']).strip()
        rainfall = str(row['rainfall']).strip()
        travel_tip = str(row['travel_tip']).strip()

        return {
            'destination': destination,
            'season': season,
            'peak_months': peak_months,
            'average_temperature': average_temperature,
            'rainfall': rainfall,
            'travel_tip': travel_tip
        }

    def is_duplicate(self, processed_data):
        return BestSeason.objects.filter(
            destination=processed_data['destination'],
            season__iexact=processed_data['season']
        ).exists()
