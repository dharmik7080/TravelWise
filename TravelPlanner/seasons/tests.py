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
