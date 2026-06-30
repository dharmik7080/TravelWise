import pandas as pd
from destinations.models import Destination
from destinations.management.commands.base_import import BaseCSVImportCommand

class Command(BaseCSVImportCommand):
    help = 'Import destinations from a CSV file using pandas'
    required_fields = [
        'destination_name', 'city', 'category', 'description', 
        'best_season', 'budget_level', 'average_cost_per_day'
    ]
    model_class = Destination
    import_type_name = "destinations"

    def process_row(self, row, row_num):
        dest_name = str(row['destination_name']).strip()
        city = str(row['city']).strip()
        state = str(row['state']).strip() if 'state' in row and not pd.isna(row['state']) else ""
        region = str(row['region']).strip() if 'region' in row and not pd.isna(row['region']) else ""
        category = str(row['category']).strip()
        description = str(row['description']).strip()
        best_season = str(row['best_season']).strip()
        
        try:
            ideal_days = int(row['ideal_days']) if 'ideal_days' in row and not pd.isna(row['ideal_days']) else 1
            if ideal_days <= 0:
                ideal_days = 1
        except (ValueError, TypeError):
            ideal_days = 1

        budget_level = str(row['budget_level']).strip()
        if budget_level not in ['Budget', 'Moderate', 'Luxury']:
            raise ValueError(f"Invalid budget level '{budget_level}'. Expected 'Budget', 'Moderate', or 'Luxury'.")

        try:
            average_cost_per_day = float(row['average_cost_per_day'])
        except (ValueError, TypeError):
            raise ValueError(f"Invalid average cost per day '{row['average_cost_per_day']}'.")

        try:
            average_rating = float(row['average_rating']) if 'average_rating' in row and not pd.isna(row['average_rating']) else 0.0
            if average_rating < 0.0 or average_rating > 5.0:
                average_rating = 0.0
        except (ValueError, TypeError):
            average_rating = 0.0

        family_friendly = bool(row['family_friendly']) if 'family_friendly' in row and not pd.isna(row['family_friendly']) else True
        couple_friendly = bool(row['couple_friendly']) if 'couple_friendly' in row and not pd.isna(row['couple_friendly']) else True
        solo_friendly = bool(row['solo_friendly']) if 'solo_friendly' in row and not pd.isna(row['solo_friendly']) else True

        return {
            'destination_name': dest_name,
            'city': city,
            'state': state,
            'region': region,
            'category': category,
            'description': description,
            'best_season': best_season,
            'ideal_days': ideal_days,
            'budget_level': budget_level,
            'average_cost_per_day': average_cost_per_day,
            'family_friendly': family_friendly,
            'couple_friendly': couple_friendly,
            'solo_friendly': solo_friendly,
            'average_rating': average_rating
        }

    def is_duplicate(self, processed_data):
        return Destination.objects.filter(destination_name__iexact=processed_data['destination_name']).exists()
