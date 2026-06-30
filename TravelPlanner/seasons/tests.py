from django.test import TestCase
from django.urls import reverse
from destinations.models import Destination
from .models import BestSeason

class BestSeasonTests(TestCase):
    """
    Test suite for best season database definitions and templates.
    """
    def setUp(self):
        self.destination = Destination.objects.create(
            destination_name="Maui",
            city="Lahaina",
            state="Hawaii",
            category="Beach",
            description="Beautiful tropical island.",
            best_season="Winter",
            ideal_days=5,
            budget_level="Expensive",
            average_cost_per_day=400.00,
            average_rating=4.9
        )
        self.best_season = BestSeason.objects.create(
            destination=self.destination,
            season="Winter",
            peak_months="December to February",
            average_temperature="26°C",
            rainfall="Moderate",
            travel_tip="Great time for whale watching off the coast."
        )

    def test_destination_details_shows_best_season(self):
        response = self.client.get(reverse('destinations:detail', kwargs={'pk': self.destination.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Winter")
        self.assertContains(response, "December to February")
        self.assertContains(response, "26°C")
        self.assertContains(response, "Great time for whale watching off the coast.")


class ImportSeasonsCommandTests(TestCase):
    def setUp(self):
        self.destination = Destination.objects.create(
            destination_name="Lahore",
            city="Lahore",
            state="Punjab",
            category="Heritage",
            description="Historic city.",
            best_season="Winter",
            ideal_days=3,
            budget_level="Budget",
            average_cost_per_day=50.00,
            average_rating=4.5
        )

    def test_import_seasons_command_success(self):
        import tempfile
        import csv
        from django.core.management import call_command

        with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as f:
            csv_path = f.name
            writer = csv.writer(f)
            writer.writerow([
                'destination_name', 'season', 'peak_months', 
                'average_temperature', 'rainfall', 'travel_tip'
            ])
            writer.writerow([
                'Lahore', 'Winter', 'Nov-Feb', '15C', 'Low', 'Enjoy historical monuments.'
            ])
        
        call_command('import_seasons', csv_path)
        self.assertEqual(BestSeason.objects.filter(destination=self.destination).count(), 1)
        self.assertTrue(BestSeason.objects.filter(season='Winter', destination=self.destination).exists())
