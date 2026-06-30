import pandas as pd
from attractions.models import Attraction
from destinations.models import Destination
from destinations.management.commands.base_import import BaseCSVImportCommand

class Command(BaseCSVImportCommand):
    help = 'Import attractions from a CSV file using pandas'
    required_fields = [
        'attraction_name', 'destination_name', 'category', 
        'description', 'opening_time', 'closing_time'
    ]
    model_class = Attraction
    import_type_name = "attractions"

    def process_row(self, row, row_num):
        attraction_name = str(row['attraction_name']).strip()
        dest_name = str(row['destination_name']).strip()

        # Retrieve destination reference by name lookup
        try:
            destination = Destination.objects.get(destination_name__iexact=dest_name)
        except Destination.DoesNotExist:
            raise ValueError(f"Destination '{dest_name}' does not exist in database.")

        category = str(row['category']).strip()
        description = str(row['description']).strip()

        try:
            entry_fee = float(row['entry_fee']) if 'entry_fee' in row and not pd.isna(row['entry_fee']) else 0.00
            if entry_fee < 0.0:
                entry_fee = 0.00
        except (ValueError, TypeError):
            entry_fee = 0.00

        opening_time = str(row['opening_time']).strip()
        closing_time = str(row['closing_time']).strip()

        try:
            average_visit_time = int(row['average_visit_time']) if 'average_visit_time' in row and not pd.isna(row['average_visit_time']) else 60
            if average_visit_time <= 0:
                average_visit_time = 60
        except (ValueError, TypeError):
            average_visit_time = 60

        return {
            'attraction_name': attraction_name,
            'destination': destination,
            'category': category,
            'description': description,
            'entry_fee': entry_fee,
            'opening_time': opening_time,
            'closing_time': closing_time,
            'average_visit_time': average_visit_time
        }

    def is_duplicate(self, processed_data):
        return Attraction.objects.filter(attraction_name__iexact=processed_data['attraction_name']).exists()
