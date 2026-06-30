from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch
from destinations.models import Destination
from .models import Trip, ItineraryTemplate, ItineraryDay

User = get_user_model()

class TripsAccessTests(TestCase):
    """
    Test suite for traveler custom Trip planning validations, access rules, and lists.
    """
    def setUp(self):
        self.username = "testuser"
        self.password = "Secr3tP@ssw0rd!"
        self.user = User.objects.create_user(
            username=self.username,
            email="testuser@example.com",
            password=self.password
        )
        self.destination = Destination.objects.create(
            destination_name="Yellowstone National Park",
            city="Wyoming",
            state="Wyoming",
            category="Nature",
            description="Geothermal wilderness area.",
            best_season="Summer",
            ideal_days=4,
            budget_level="Moderate",
            average_cost_per_day=180.00,
            average_rating=4.7
        )

    def test_trips_page_login_required(self):
        response = self.client.get(reverse('trips:index'))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('trips:index')}")

    def test_trips_page_loads_for_authenticated_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('trips:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trips/index.html')

    def test_plan_trip_page_login_required(self):
        response = self.client.get(reverse('trips:plan'))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('trips:plan')}")

    def test_plan_trip_page_loads_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('trips:plan'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trips/trip_form.html')

    def test_plan_trip_validation_end_date_after_start_date(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('trips:plan'), {
            'destination': self.destination.pk,
            'start_date': '2026-07-10',
            'end_date': '2026-07-09',  # end_date is before start_date
            'number_of_travelers': 2,
            'budget': 500.00,
            'travel_type': 'Couple',
            'notes': 'test'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'end_date', "End date must be after the start date.")

    def test_plan_trip_validation_budget_positive(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('trips:plan'), {
            'destination': self.destination.pk,
            'start_date': '2026-07-10',
            'end_date': '2026-07-15',
            'number_of_travelers': 2,
            'budget': 0.00,  # invalid budget
            'travel_type': 'Couple',
            'notes': 'test'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'budget', "Budget must be a positive number.")

    def test_plan_trip_validation_travelers_at_least_1(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('trips:plan'), {
            'destination': self.destination.pk,
            'start_date': '2026-07-10',
            'end_date': '2026-07-15',
            'number_of_travelers': 0,  # invalid travelers count
            'budget': 500.00,
            'travel_type': 'Couple',
            'notes': 'test'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'number_of_travelers', "Number of travelers must be at least 1.")

    def test_plan_trip_success_creates_trip(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('trips:plan'), {
            'destination': self.destination.pk,
            'start_date': '2026-07-10',
            'end_date': '2026-07-15',
            'number_of_travelers': 3,
            'budget': 1500.00,
            'travel_type': 'Family',
            'notes': 'Trip notes.'
        })
        self.assertRedirects(response, reverse('trips:index'))
        self.assertEqual(Trip.objects.count(), 1)
        trip = Trip.objects.first()
        self.assertEqual(trip.destination, self.destination)
        self.assertEqual(trip.user, self.user)
        self.assertEqual(trip.number_of_travelers, 3)
        self.assertEqual(trip.budget, 1500.00)
        self.assertEqual(trip.travel_type, 'Family')

    def test_trip_detail_view_owner(self):
        self.client.login(username=self.username, password=self.password)
        trip = Trip.objects.create(
            user=self.user,
            destination=self.destination,
            start_date='2026-07-10',
            end_date='2026-07-15',
            number_of_travelers=2,
            budget=500.00,
            travel_type='Couple'
        )
        response = self.client.get(reverse('trips:detail', kwargs={'pk': trip.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['trip'], trip)

    def test_trip_detail_view_non_owner_returns_404(self):
        # Create another user who will own the trip
        other_user = User.objects.create_user(username="other", email="other@example.com", password="password")
        trip = Trip.objects.create(
            user=other_user,
            destination=self.destination,
            start_date='2026-07-10',
            end_date='2026-07-15',
            number_of_travelers=2,
            budget=500.00,
            travel_type='Couple'
        )
        # Login as the first user and try to view the trip
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('trips:detail', kwargs={'pk': trip.pk}))
        self.assertEqual(response.status_code, 404)

    def test_trip_update_view_owner(self):
        self.client.login(username=self.username, password=self.password)
        trip = Trip.objects.create(
            user=self.user,
            destination=self.destination,
            start_date='2026-07-10',
            end_date='2026-07-15',
            number_of_travelers=2,
            budget=500.00,
            travel_type='Couple'
        )
        response = self.client.post(reverse('trips:update', kwargs={'pk': trip.pk}), {
            'destination': self.destination.pk,
            'start_date': '2026-07-10',
            'end_date': '2026-07-18',  # Changed end date
            'number_of_travelers': 4,   # Changed travelers count
            'budget': 800.00,           # Changed budget
            'travel_type': 'Family'
        })
        self.assertRedirects(response, reverse('trips:index'))
        trip.refresh_from_db()
        self.assertEqual(trip.number_of_travelers, 4)
        self.assertEqual(trip.budget, 800.00)
        self.assertEqual(trip.travel_type, 'Family')

    def test_trip_update_view_non_owner_returns_404(self):
        other_user = User.objects.create_user(username="other", email="other@example.com", password="password")
        trip = Trip.objects.create(
            user=other_user,
            destination=self.destination,
            start_date='2026-07-10',
            end_date='2026-07-15',
            number_of_travelers=2,
            budget=500.00,
            travel_type='Couple'
        )
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('trips:update', kwargs={'pk': trip.pk}), {
            'destination': self.destination.pk,
            'start_date': '2026-07-10',
            'end_date': '2026-07-18',
            'number_of_travelers': 4,
            'budget': 800.00,
            'travel_type': 'Family'
        })
        self.assertEqual(response.status_code, 404)

    def test_trip_delete_view_owner(self):
        self.client.login(username=self.username, password=self.password)
        trip = Trip.objects.create(
            user=self.user,
            destination=self.destination,
            start_date='2026-07-10',
            end_date='2026-07-15',
            number_of_travelers=2,
            budget=500.00,
            travel_type='Couple'
        )
        response = self.client.post(reverse('trips:delete', kwargs={'pk': trip.pk}))
        self.assertRedirects(response, reverse('trips:index'))
        self.assertEqual(Trip.objects.filter(pk=trip.pk).count(), 0)

    def test_trip_delete_view_non_owner_returns_404(self):
        other_user = User.objects.create_user(username="other", email="other@example.com", password="password")
        trip = Trip.objects.create(
            user=other_user,
            destination=self.destination,
            start_date='2026-07-10',
            end_date='2026-07-15',
            number_of_travelers=2,
            budget=500.00,
            travel_type='Couple'
        )
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('trips:delete', kwargs={'pk': trip.pk}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Trip.objects.filter(pk=trip.pk).count(), 1)

    def test_trips_pagination_limit(self):
        self.client.login(username=self.username, password=self.password)
        # Create 9 trips for the user
        for i in range(9):
            Trip.objects.create(
                user=self.user,
                destination=self.destination,
                start_date='2026-07-10',
                end_date='2026-07-15',
                number_of_travelers=1,
                budget=100.00,
                travel_type='Solo'
            )
        response = self.client.get(reverse('trips:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['trips']), 8)  # Paginated at 8 items
        self.assertTrue(response.context['is_paginated'])

    @patch('trips.views.get_current_weather')
    def test_trip_detail_view_weather_rendering(self, mock_get_weather):
        mock_get_weather.return_value = {
            'temp': 22,
            'condition': 'Cloudy',
            'humidity': 55,
            'wind_speed': 3.2,
            'icon': '03d'
        }
        self.client.login(username=self.username, password=self.password)
        trip = Trip.objects.create(
            user=self.user,
            destination=self.destination,
            start_date='2026-07-10',
            end_date='2026-07-15',
            number_of_travelers=2,
            budget=500.00,
            travel_type='Couple'
        )
        response = self.client.get(reverse('trips:detail', kwargs={'pk': trip.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "22°C")
        self.assertContains(response, "Cloudy")
        self.assertContains(response, "Humidity")
        self.assertContains(response, "55%")

    def test_itinerary_generation_with_templates(self):
        # Create predefined templates
        ItineraryTemplate.objects.create(
            destination=self.destination,
            day_number=1,
            morning="Visit Attraction 1",
            afternoon="Lunch & Explore Market",
            evening="Local Food"
        )
        ItineraryTemplate.objects.create(
            destination=self.destination,
            day_number=2,
            morning="Beach Day",
            afternoon="Museum Tour",
            evening="Shopping"
        )
        
        self.client.login(username=self.username, password=self.password)
        # Create a 2-day trip
        response = self.client.post(reverse('trips:plan'), {
            'destination': self.destination.pk,
            'start_date': '2026-07-10',
            'end_date': '2026-07-11',
            'number_of_travelers': 2,
            'budget': 500.00,
            'travel_type': 'Couple',
            'notes': 'test'
        })
        self.assertRedirects(response, reverse('trips:index'))
        
        trip = Trip.objects.first()
        self.assertEqual(trip.itinerary_days.count(), 2)
        day1 = trip.itinerary_days.get(day_number=1)
        self.assertEqual(day1.morning, "Visit Attraction 1")
        self.assertEqual(day1.afternoon, "Lunch & Explore Market")
        self.assertEqual(day1.evening, "Local Food")
        day2 = trip.itinerary_days.get(day_number=2)
        self.assertEqual(day2.morning, "Beach Day")

    def test_itinerary_generation_cycling(self):
        # Create only 1 template day
        ItineraryTemplate.objects.create(
            destination=self.destination,
            day_number=1,
            morning="Visit Attraction 1",
            afternoon="Lunch & Explore Market",
            evening="Local Food"
        )
        self.client.login(username=self.username, password=self.password)
        # Create a 2-day trip; day 2 should cycle back to day 1's template
        self.client.post(reverse('trips:plan'), {
            'destination': self.destination.pk,
            'start_date': '2026-07-10',
            'end_date': '2026-07-11',
            'number_of_travelers': 2,
            'budget': 500.00,
            'travel_type': 'Couple',
            'notes': 'test'
        })
        trip = Trip.objects.first()
        self.assertEqual(trip.itinerary_days.count(), 2)
        day1 = trip.itinerary_days.get(day_number=1)
        day2 = trip.itinerary_days.get(day_number=2)
        self.assertEqual(day1.morning, "Visit Attraction 1")
        self.assertEqual(day2.morning, "Visit Attraction 1")

    def test_itinerary_generation_fallback(self):
        # No templates created
        self.client.login(username=self.username, password=self.password)
        self.client.post(reverse('trips:plan'), {
            'destination': self.destination.pk,
            'start_date': '2026-07-10',
            'end_date': '2026-07-11',
            'number_of_travelers': 2,
            'budget': 500.00,
            'travel_type': 'Couple',
            'notes': 'test'
        })
        trip = Trip.objects.first()
        self.assertEqual(trip.itinerary_days.count(), 2)
        day1 = trip.itinerary_days.get(day_number=1)
        self.assertEqual(day1.morning, "Explore local spots and landmarks")

    def test_itinerary_edit_view_permissions_and_update(self):
        self.client.login(username=self.username, password=self.password)
        trip = Trip.objects.create(
            user=self.user,
            destination=self.destination,
            start_date='2026-07-10',
            end_date='2026-07-11',
            number_of_travelers=2,
            budget=500.00,
            travel_type='Couple'
        )
        # Create itinerary days
        day1 = ItineraryDay.objects.create(
            trip=trip,
            day_number=1,
            morning="Old Morning",
            afternoon="Old Afternoon",
            evening="Old Evening"
        )
        day2 = ItineraryDay.objects.create(
            trip=trip,
            day_number=2,
            morning="Old Morning 2",
            afternoon="Old Afternoon 2",
            evening="Old Evening 2"
        )
        
        # Test anonymous access redirects
        self.client.logout()
        response = self.client.get(reverse('trips:edit_itinerary', kwargs={'pk': trip.pk}))
        self.assertEqual(response.status_code, 302)
        
        # Test non-owner access returns 404
        other_user = User.objects.create_user(username="other", email="other@example.com", password="password")
        self.client.login(username="other", password="password")
        response = self.client.get(reverse('trips:edit_itinerary', kwargs={'pk': trip.pk}))
        self.assertEqual(response.status_code, 404)
        
        # Test owner can access edit page
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('trips:edit_itinerary', kwargs={'pk': trip.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trips/itinerary_form.html')
        
        # Test batch update via formset
        response = self.client.post(reverse('trips:edit_itinerary', kwargs={'pk': trip.pk}), {
            'itinerary_days-TOTAL_FORMS': 2,
            'itinerary_days-INITIAL_FORMS': 2,
            'itinerary_days-MIN_NUM_FORMS': 0,
            'itinerary_days-MAX_NUM_FORMS': 1000,
            'itinerary_days-0-id': day1.pk,
            'itinerary_days-0-morning': "New Morning 1",
            'itinerary_days-0-afternoon': "New Afternoon 1",
            'itinerary_days-0-evening': "New Evening 1",
            'itinerary_days-1-id': day2.pk,
            'itinerary_days-1-morning': "New Morning 2",
            'itinerary_days-1-afternoon': "New Afternoon 2",
            'itinerary_days-1-evening': "New Evening 2",
        })
        self.assertRedirects(response, reverse('trips:detail', kwargs={'pk': trip.pk}))
        day1.refresh_from_db()
        day2.refresh_from_db()
        self.assertEqual(day1.morning, "New Morning 1")
        self.assertEqual(day2.morning, "New Morning 2")


class TripAdminTests(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User
        self.username = "admin"
        self.password = "adminpass"
        self.admin_user = User.objects.create_superuser(
            username=self.username,
            email="admin@example.com",
            password=self.password
        )
        self.user = User.objects.create_user(
            username="traveller_jane",
            password="jane_password",
            email="jane@example.com"
        )
        self.destination = Destination.objects.create(
            destination_name="Yosemite Valley Admin",
            city="Yosemite",
            state="California",
            category="Nature",
            description="Scenic valley.",
            best_season="Summer",
            ideal_days=3,
            budget_level="Moderate",
            average_cost_per_day=200.00,
            average_rating=4.9
        )
        self.trip = Trip.objects.create(
            user=self.user,
            destination=self.destination,
            start_date='2026-07-15',
            end_date='2026-07-20',
            number_of_travelers=2,
            budget=800.00,
            travel_type='Couple'
        )

    def test_trip_admin_list_display_and_features(self):
        from django.contrib.admin.sites import site
        from .admin import TripAdmin, TripStatusListFilter
        
        self.assertIn(Trip, site._registry)
        admin_instance = site._registry[Trip]
        self.assertIsInstance(admin_instance, TripAdmin)
        
        expected_list_display = ('get_username', 'destination', 'start_date', 'end_date', 'budget', 'travel_type')
        self.assertEqual(admin_instance.list_display, expected_list_display)
        
        expected_search_fields = ('user__username', 'destination__destination_name')
        self.assertEqual(admin_instance.search_fields, expected_search_fields)
        
        # Test get_username returns correct string
        self.assertEqual(admin_instance.get_username(self.trip), "traveller_jane")
        
        # Test custom TripStatusListFilter lookups
        filter_instance = TripStatusListFilter(None, {'status': 'upcoming'}, Trip, admin_instance)
        lookups = filter_instance.lookups(None, admin_instance)
        self.assertEqual(lookups, (('upcoming', 'Upcoming'), ('completed', 'Completed')))

    def test_trip_admin_queryset_optimization(self):
        from django.contrib.admin.sites import site
        admin_instance = site._registry[Trip]
        
        request = None
        queryset = admin_instance.get_queryset(request)
        # Check select_related has 'user' and 'destination'
        self.assertTrue(queryset.query.select_related)
        self.assertIn('user', queryset.query.select_related)
        self.assertIn('destination', queryset.query.select_related)


class TripCSVExportTests(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User
        self.username = "admin"
        self.password = "adminpass"
        self.admin_user = User.objects.create_superuser(
            username=self.username,
            email="admin@example.com",
            password=self.password
        )
        self.user = User.objects.create_user(
            username="traveller_jane",
            password="jane_password",
            email="jane@example.com"
        )
        self.destination = Destination.objects.create(
            destination_name="Yosemite Valley Admin Export",
            city="Yosemite",
            state="California",
            category="Nature",
            description="Scenic valley.",
            best_season="Summer",
            ideal_days=3,
            budget_level="Moderate",
            average_cost_per_day=200.00,
            average_rating=4.9
        )
        self.trip = Trip.objects.create(
            user=self.user,
            destination=self.destination,
            start_date='2026-07-15',
            end_date='2026-07-20',
            number_of_travelers=2,
            budget=800.00,
            travel_type='Couple'
        )

    def test_trip_csv_export_requires_staff(self):
        response = self.client.get('/admin/trips/trip/export-csv/')
        self.assertEqual(response.status_code, 302)

    def test_trip_csv_export_success(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/admin/trips/trip/export-csv/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('attachment; filename="trips.csv"', response['Content-Disposition'])
        
        content = b"".join(response.streaming_content).decode('utf-8')
        self.assertIn("user__username", content)
        self.assertIn("destination__destination_name", content)
        self.assertIn("traveller_jane", content)
        self.assertIn("Yosemite Valley Admin Export", content)
        self.assertIn("Couple", content)


class TripModelValidationTests(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User
        self.user = User.objects.create_user(username="valid_user", password="valid_password")
        self.destination = Destination.objects.create(
            destination_name="Yosemite Valley Validated",
            city="Yosemite",
            state="California",
            category="Nature",
            description="Scenic valley.",
            best_season="Summer",
            ideal_days=3,
            budget_level="Moderate",
            average_cost_per_day=200.00,
            average_rating=4.9
        )

    def test_trip_validation_dates_order(self):
        from django.core.exceptions import ValidationError
        trip = Trip(
            user=self.user,
            destination=self.destination,
            start_date='2026-07-20',
            end_date='2026-07-15',  # End before start
            number_of_travelers=2,
            budget=800.00,
            travel_type='Couple'
        )
        with self.assertRaises(ValidationError):
            trip.clean()

    def test_trip_validation_negative_budget(self):
        from django.core.exceptions import ValidationError
        trip = Trip(
            user=self.user,
            destination=self.destination,
            start_date='2026-07-15',
            end_date='2026-07-20',
            number_of_travelers=2,
            budget=-800.00,  # Negative budget
            travel_type='Couple'
        )
        with self.assertRaises(ValidationError):
            trip.clean()

    def test_trip_validation_negative_travelers(self):
        from django.core.exceptions import ValidationError
        trip = Trip(
            user=self.user,
            destination=self.destination,
            start_date='2026-07-15',
            end_date='2026-07-20',
            number_of_travelers=0,  # Invalid traveler count
            budget=800.00,
            travel_type='Couple'
        )
        with self.assertRaises(ValidationError):
            trip.clean()

    def test_itinerary_template_validation_day_number(self):
        from django.core.exceptions import ValidationError
        template = ItineraryTemplate(
            destination=self.destination,
            day_number=0,  # Invalid day number
            morning="Morning",
            afternoon="Afternoon",
            evening="Evening"
        )
        with self.assertRaises(ValidationError):
            template.clean()



