import pandas as pd
from packages.models import Package
from destinations.models import Destination
from destinations.management.commands.base_import import BaseCSVImportCommand

class Command(BaseCSVImportCommand):
    help = 'Import travel packages from a CSV file using pandas'
    required_fields = [
        'package_name', 'destination_name', 'package_type', 
        'price', 'description'
    ]
    model_class = Package
    import_type_name = "packages"

    def process_row(self, row, row_num):
        package_name = str(row['package_name']).strip()
        dest_name = str(row['destination_name']).strip()

        # Retrieve destination reference by name lookup
        try:
            destination = Destination.objects.get(destination_name__iexact=dest_name)
        except Destination.DoesNotExist:
            raise ValueError(f"Destination '{dest_name}' does not exist in database.")

        try:
            duration = int(row['duration']) if 'duration' in row and not pd.isna(row['duration']) else 1
            if duration <= 0:
                duration = 1
        except (ValueError, TypeError):
            duration = 1

        package_type = str(row['package_type']).strip()

        try:
            price = float(row['price'])
            if price < 0.0:
                raise ValueError("Price cannot be negative.")
        except (ValueError, TypeError):
            raise ValueError(f"Invalid price value '{row['price']}'.")

        description = str(row['description']).strip()

        return {
            'package_name': package_name,
            'destination': destination,
            'duration': duration,
            'package_type': package_type,
            'price': price,
            'description': description
        }

    def is_duplicate(self, processed_data):
        return Package.objects.filter(package_name__iexact=processed_data['package_name']).exists()
