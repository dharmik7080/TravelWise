import os
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from destinations.models import Destination

class Command(BaseCommand):
    help = 'Import destinations from a CSV file using pandas'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file to import')

    def handle(self, *args, **options):
        csv_path = options['csv_file']

        if not os.path.exists(csv_path):
            raise CommandError(f"CSV file not found at: {csv_path}")

        try:
            # Read CSV using pandas
            df = pd.read_csv(csv_path)
        except Exception as e:
            raise CommandError(f"Failed to read CSV file: {e}")

        required_fields = [
            'destination_name', 'city', 'category', 'description', 
            'best_season', 'budget_level', 'average_cost_per_day'
        ]

        total_rows = len(df)
        success_count = 0
        skipped_duplicates = 0
        skipped_invalid = 0
        error_details = []

        self.stdout.write(f"Starting import of {total_rows} destinations...")

        for index, row in df.iterrows():
            row_num = index + 1
            
            # 1. Check for missing required fields
            missing = [field for field in required_fields if pd.isna(row[field]) or str(row[field]).strip() == '']
            if missing:
                skipped_invalid += 1
                error_details.append(f"Row {row_num}: Missing required fields: {', '.join(missing)}")
                continue

            dest_name = str(row['destination_name']).strip()
            city = str(row['city']).strip()
            state = str(row['state']).strip() if not pd.isna(row['state']) else ""
            region = str(row['region']).strip() if not pd.isna(row['region']) else ""
            category = str(row['category']).strip() if not pd.isna(row['category']) else ""
            description = str(row['description']).strip()
            best_season = str(row['best_season']).strip()
            
            try:
                ideal_days = int(row['ideal_days']) if not pd.isna(row['ideal_days']) else 1
                if ideal_days <= 0:
                    ideal_days = 1
            except (ValueError, TypeError):
                ideal_days = 1

            budget_level = str(row['budget_level']).strip()
            if budget_level not in ['Budget', 'Moderate', 'Luxury']:
                skipped_invalid += 1
                error_details.append(f"Row {row_num}: Invalid budget level '{budget_level}'. Expected 'Budget', 'Moderate', or 'Luxury'.")
                continue

            try:
                average_cost_per_day = float(row['average_cost_per_day'])
            except (ValueError, TypeError):
                skipped_invalid += 1
                error_details.append(f"Row {row_num}: Invalid average cost per day '{row['average_cost_per_day']}'.")
                continue

            try:
                average_rating = float(row['average_rating']) if not pd.isna(row['average_rating']) else 0.0
                if average_rating < 0.0 or average_rating > 5.0:
                    average_rating = 0.0
            except (ValueError, TypeError):
                average_rating = 0.0

            family_friendly = bool(row['family_friendly']) if not pd.isna(row['family_friendly']) else True
            couple_friendly = bool(row['couple_friendly']) if not pd.isna(row['couple_friendly']) else True
            solo_friendly = bool(row['solo_friendly']) if not pd.isna(row['solo_friendly']) else True

            # 2. Ignore duplicate destinations (by checking database)
            if Destination.objects.filter(destination_name__iexact=dest_name).exists():
                skipped_duplicates += 1
                continue

            # 3. Insert data using Django ORM
            try:
                Destination.objects.create(
                    destination_name=dest_name,
                    city=city,
                    state=state,
                    region=region,
                    category=category,
                    description=description,
                    best_season=best_season,
                    ideal_days=ideal_days,
                    budget_level=budget_level,
                    average_cost_per_day=average_cost_per_day,
                    family_friendly=family_friendly,
                    couple_friendly=couple_friendly,
                    solo_friendly=solo_friendly,
                    average_rating=average_rating
                )
                success_count += 1
            except IntegrityError:
                skipped_duplicates += 1
            except Exception as e:
                skipped_invalid += 1
                error_details.append(f"Row {row_num}: Error creating destination: {e}")

        # Summary Display
        self.stdout.write(self.style.SUCCESS("\n--- Import Summary ---"))
        self.stdout.write(f"Total Rows Processed: {total_rows}")
        self.stdout.write(self.style.SUCCESS(f"Successfully Imported: {success_count}"))
        self.stdout.write(self.style.WARNING(f"Skipped Duplicates: {skipped_duplicates}"))
        self.stdout.write(self.style.ERROR(f"Skipped Invalid / Erroneous: {skipped_invalid}"))
        
        if error_details:
            self.stdout.write("\n--- Validation Errors ---")
            for err in error_details:
                self.stdout.write(self.style.ERROR(err))
