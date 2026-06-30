import os
import pandas as pd
from django.core.management.base import BaseCommand, CommandError

class BaseCSVImportCommand(BaseCommand):
    """
    Abstract base command for importing CSV datasets using pandas.
    """
    # Subclasses must override these configuration attributes:
    required_fields = []
    model_class = None
    import_type_name = "records"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file to import')

    def handle(self, *args, **options):
        csv_path = options['csv_file']

        if not os.path.exists(csv_path):
            raise CommandError(f"CSV file not found at: {csv_path}")

        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            raise CommandError(f"Failed to read CSV file: {e}")

        total_rows = len(df)
        success_count = 0
        skipped_duplicates = 0
        skipped_invalid = 0
        error_details = []

        self.stdout.write(f"Starting import of {total_rows} {self.import_type_name}...")

        for index, row in df.iterrows():
            row_num = index + 1
            
            # Validate required columns exist and are non-empty
            missing = [field for field in self.required_fields if field not in row or pd.isna(row[field]) or str(row[field]).strip() == '']
            if missing:
                skipped_invalid += 1
                error_details.append(f"Row {row_num}: Missing required fields: {', '.join(missing)}")
                continue

            # Process record row
            try:
                processed_data = self.process_row(row, row_num)
                if processed_data is None:
                    # process_row returned None indicating validation failure
                    skipped_invalid += 1
                    continue
                
                # Check for duplicates
                if self.is_duplicate(processed_data):
                    skipped_duplicates += 1
                    continue

                # Save record
                self.save_record(processed_data)
                success_count += 1
            except Exception as e:
                skipped_invalid += 1
                error_details.append(f"Row {row_num}: {e}")

        # Summary Display
        self.stdout.write(self.style.SUCCESS(f"\n--- Import Summary ---"))
        self.stdout.write(f"Total Rows Processed: {total_rows}")
        self.stdout.write(self.style.SUCCESS(f"Successfully Imported: {success_count}"))
        self.stdout.write(self.style.WARNING(f"Skipped Duplicates: {skipped_duplicates}"))
        self.stdout.write(self.style.ERROR(f"Skipped Invalid / Erroneous: {skipped_invalid}"))
        
        if error_details:
            self.stdout.write("\n--- Validation Errors ---")
            for err in error_details:
                self.stdout.write(self.style.ERROR(err))

    def process_row(self, row, row_num):
        """Must return a dictionary of cleaned data, or raise an exception/return None."""
        raise NotImplementedError("Subclasses must implement process_row()")

    def is_duplicate(self, processed_data):
        """Return True if duplicate, False otherwise."""
        raise NotImplementedError("Subclasses must implement is_duplicate()")

    def save_record(self, processed_data):
        """Create database object."""
        self.model_class.objects.create(**processed_data)
