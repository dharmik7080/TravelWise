from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch

class DashboardAccessTests(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "Secr3tP@ssw0rd!"
        self.user = User.objects.create_user(
            username=self.username,
            email="testuser@example.com",
            password=self.password
        )

    def test_dashboard_page_login_required(self):
        # Unauthenticated user should be redirected to login
        response = self.client.get(reverse('dashboard:index'))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('dashboard:index')}")

    def test_dashboard_page_loads_for_authenticated_user(self):
        # Authenticated user should load dashboard successfully
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')

    def test_predictions_page_login_required(self):
        # Unauthenticated user should be redirected to login
        response = self.client.get(reverse('dashboard:predictions'))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('dashboard:predictions')}")

    def test_predictions_page_loads_for_authenticated_user(self):
        # Authenticated user should load predictions page successfully
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('dashboard:predictions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/predictions.html')

    @patch('django.utils.timezone.now')
    def test_dashboard_statistics_and_lists(self, mock_now):
        import datetime
        from django.utils import timezone
        mock_now.return_value = timezone.make_aware(datetime.datetime(2026, 6, 30, 10, 0, 0))
        
        from destinations.models import Destination
        from trips.models import Trip
        
        # Create a destination spot
        dest = Destination.objects.create(
            destination_name="Yosemite Valley",
            city="Mariposa",
            state="California",
            category="Nature",
            description="Glacial valley in California.",
            best_season="Spring",
            ideal_days=3,
            budget_level="Moderate",
            average_cost_per_day=150.00,
            average_rating=4.9
        )
        
        # Create a planned trip (upcoming)
        Trip.objects.create(
            user=self.user,
            destination=dest,
            start_date='2026-07-15',
            end_date='2026-07-20',
            number_of_travelers=2,
            budget=800.00,
            travel_type='Couple'
        )
        
        # Create a planned trip (past/recent)
        Trip.objects.create(
            user=self.user,
            destination=dest,
            start_date='2026-05-10',
            end_date='2026-05-15',
            number_of_travelers=1,
            budget=300.00,
            travel_type='Solo'
        )
        
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 200)
        
        # Assert stats context keys
        self.assertEqual(response.context['total_trips'], 2)
        self.assertEqual(response.context['upcoming_count'], 1)
        self.assertEqual(response.context['completed_count'], 1)
        self.assertEqual(response.context['average_budget'], 550.00)
        
        # Assert lists
        self.assertEqual(len(response.context['upcoming_trips']), 1)
        self.assertEqual(len(response.context['recent_trips']), 2)
        
        # Assert remaining days property calculation
        upcoming_trip = response.context['upcoming_trips'][0]
        # From June 30, 2026 (current time) to July 15, 2026 is exactly 15 days
        self.assertEqual(upcoming_trip.remaining_days, 15)
        
        # Assert rendered elements on HTML page
        self.assertContains(response, "Yosemite Valley")
        self.assertContains(response, "Total Trips")
        self.assertContains(response, "Smart Travel Tips")
        self.assertContains(response, "Travel Spending & Insights")
        self.assertContains(response, "15 Days Left")
        self.assertContains(response, 'href="/trips/plan/"')
        self.assertContains(response, 'href="/destinations/"')
        self.assertContains(response, 'href="/trips/"')
        self.assertContains(response, 'href="/packages/"')
        self.assertTrue(response.context['has_charts'])
        # Confirms the plotly component got injected into the page response
        self.assertContains(response, 'class="plotly-graph-div"')

        # Assert Travel Insights context values
        self.assertEqual(response.context['most_visited_dest'], "Yosemite Valley")
        self.assertEqual(float(response.context['highest_budget_trip'].budget), 800.00)
        self.assertEqual(response.context['avg_duration_days'], 6)
        self.assertIn(response.context['most_common_type'], ['Couple', 'Solo'])

        # Assert Travel Insights rendered elements
        self.assertContains(response, "Most Visited")
        self.assertContains(response, "Highest Budget")
        self.assertContains(response, "Avg. Duration")
        self.assertContains(response, "Common Type")
        self.assertContains(response, "6 Days")
        self.assertContains(response, "$800")

    def test_dashboard_empty_charts(self):
        # Authenticated user with 0 planned trips
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['has_charts'])
        self.assertContains(response, "Analytics Visualizations Placeholder")
        self.assertNotContains(response, 'class="plotly-graph-div"')
        
        # Assert empty state message for Travel Insights
        self.assertContains(response, "No travel insights available yet. Plan some trips to view your travel habits!")


class AdminHomepageTests(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User
        self.username = "admin"
        self.password = "adminpass"
        self.admin_user = User.objects.create_superuser(
            username=self.username,
            email="admin@example.com",
            password=self.password
        )

    def test_admin_homepage_custom_metrics_and_shortcuts(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_users', response.context)
        self.assertIn('total_destinations', response.context)
        self.assertIn('total_trips', response.context)
        self.assertIn('total_packages', response.context)

        # Check values
        self.assertEqual(response.context['total_users'], 1)
        self.assertEqual(response.context['total_destinations'], 0)

        # Check HTML renders correctly
        self.assertContains(response, "TravelPlanner Quick Statistics")
        self.assertContains(response, "Quick Management Shortcuts")
        self.assertContains(response, "Manage Destinations")
        self.assertContains(response, "Manage Trips")

