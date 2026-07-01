from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from destinations.models import Destination
from attractions.models import Attraction
from packages.models import Package
from seasons.models import BestSeason
from trips.models import Trip, ItineraryDay, ItineraryTemplate

User = get_user_model()

class APITests(APITestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='traveller1', password='password123')
        self.user2 = User.objects.create_user(username='traveller2', password='password123')

        # Create destination
        self.destination = Destination.objects.create(
            destination_name="Goa Beach",
            city="Panaji",
            state="Goa",
            category="Beach",
            description="Lovely sunny beaches.",
            best_season="Winter",
            ideal_days=3,
            budget_level="Moderate",
            average_cost_per_day=4500.00
        )

        # Create itinerary template
        self.template1 = ItineraryTemplate.objects.create(
            destination=self.destination,
            day_number=1,
            morning="Relax on Calangute Beach",
            afternoon="Enjoy Konkani seafood lunch",
            evening="Watch sunset at Chapora Fort"
        )

    def test_public_read_destination(self):
        # Anyone can view destinations
        url = reverse('destination-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_anonymous_write_destination_fails(self):
        # Anonymous users cannot write
        url = reverse('destination-list')
        data = {
            'destination_name': 'New Spot',
            'city': 'New City',
            'category': 'Hill Station',
            'description': 'Nice view',
            'best_season': 'Summer',
            'ideal_days': 2,
            'budget_level': 'Budget',
            'average_cost_per_day': '1500.00'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_trip_creation_auto_generates_itinerary_days(self):
        # Must be authenticated
        self.client.login(username='traveller1', password='password123')

        url = reverse('trip-list')
        data = {
            'destination': self.destination.destination_id,
            'start_date': '2026-10-10',
            'end_date': '2026-10-12', # 3 days total
            'number_of_travelers': 2,
            'budget': '15000.00',
            'travel_type': 'Couple'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert trip belongs to traveller1
        trip = Trip.objects.first()
        self.assertEqual(trip.user, self.user1)

        # Assert 3 ItineraryDays were automatically created
        itineraries = ItineraryDay.objects.filter(trip=trip).order_by('day_number')
        self.assertEqual(itineraries.count(), 3)
        self.assertEqual(itineraries[0].morning, self.template1.morning) # template match
        self.assertEqual(itineraries[1].morning, self.template1.morning) # cycled match

    def test_trip_creation_generic_fallback(self):
        # Create a destination with no itinerary templates
        destination2 = Destination.objects.create(
            destination_name="Hampi Heritage",
            city="Hampi",
            state="Karnataka",
            category="Heritage",
            description="Ancient ruins.",
            best_season="Winter",
            ideal_days=2,
            budget_level="Budget",
            average_cost_per_day=2000.00
        )

        self.client.login(username='traveller1', password='password123')

        url = reverse('trip-list')
        data = {
            'destination': destination2.destination_id,
            'start_date': '2026-11-01',
            'end_date': '2026-11-02', # 2 days total
            'number_of_travelers': 1,
            'budget': '5000.00',
            'travel_type': 'Solo'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        trip = Trip.objects.filter(destination=destination2).first()
        itineraries = ItineraryDay.objects.filter(trip=trip).order_by('day_number')
        self.assertEqual(itineraries.count(), 2)
        self.assertEqual(itineraries[0].morning, "Explore local spots and landmarks") # generic fallback

    def test_trip_isolation(self):
        # traveller1 creates a trip
        trip = Trip.objects.create(
            user=self.user1,
            destination=self.destination,
            start_date='2026-12-01',
            end_date='2026-12-03',
            number_of_travelers=1,
            budget=8000.00,
            travel_type='Solo'
        )

        # traveller2 logs in
        self.client.login(username='traveller2', password='password123')

        # Retrieve trips list
        url = reverse('trip-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0) # traveller2 should not see traveller1's trip

        # Access detail directly
        detail_url = reverse('trip-detail', kwargs={'pk': trip.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) # treated as not found/inaccessible

    def test_authenticated_non_staff_write_destination_fails(self):
        # Authenticated non-staff users cannot write destinations
        self.client.login(username='traveller1', password='password123')
        url = reverse('destination-list')
        data = {
            'destination_name': 'New Spot 2',
            'city': 'New City 2',
            'category': 'Beach',
            'description': 'Nice beach',
            'best_season': 'Summer',
            'ideal_days': 2,
            'budget_level': 'Moderate',
            'average_cost_per_day': '2500.00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_staff_write_destination_success(self):
        # Create a staff user
        staff_user = User.objects.create_superuser(username='staffadmin', password='password123', email='admin@test.com')
        self.client.login(username='staffadmin', password='password123')

        url = reverse('destination-list')
        data = {
            'destination_name': 'Manali Hills',
            'city': 'Manali',
            'state': 'Himachal Pradesh',
            'category': 'Hill Station',
            'description': 'Beautiful snow-clad peaks.',
            'best_season': 'Summer',
            'ideal_days': 4,
            'budget_level': 'Moderate',
            'average_cost_per_day': '3500.00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check detail endpoint
        detail_url = reverse('destination-detail', kwargs={'pk': response.data['destination_id']})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['destination_name'], 'Manali Hills')

        # Update destination
        update_data = {
            'destination_name': 'Manali Hills Updated',
            'city': 'Manali',
            'state': 'Himachal Pradesh',
            'category': 'Hill Station',
            'description': 'Beautiful snow-clad peaks.',
            'best_season': 'Summer',
            'ideal_days': 5,
            'budget_level': 'Moderate',
            'average_cost_per_day': '4000.00'
        }
        response = self.client.put(detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ideal_days'], 5)

        # Delete destination
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destination_search_filtering_ordering(self):
        # Create multiple destinations for testing listing
        Destination.objects.create(
            destination_name="Shimla Snow",
            city="Shimla",
            state="Himachal Pradesh",
            category="Hill Station",
            description="Chilly winter hub.",
            best_season="Winter",
            ideal_days=3,
            budget_level="Budget",
            average_cost_per_day=3000.00
        )
        Destination.objects.create(
            destination_name="Alleppey Backwaters",
            city="Alappuzha",
            state="Kerala",
            category="Nature",
            description="Lovely houseboats.",
            best_season="Winter",
            ideal_days=2,
            budget_level="Luxury",
            average_cost_per_day=6000.00
        )

        url = reverse('destination-list')

        # Test search
        response = self.client.get(url + '?search=Backwaters')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['destination_name'], 'Alleppey Backwaters')

        # Test filter
        response = self.client.get(url + '?category=Hill+Station')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['destination_name'], 'Shimla Snow')

        # Test ordering (cost ascending)
        response = self.client.get(url + '?ordering=average_cost_per_day')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        # shimla is 3000, goa is 4500, alleppey is 6000
        self.assertEqual(results[0]['destination_name'], 'Shimla Snow')
        self.assertEqual(results[2]['destination_name'], 'Alleppey Backwaters')

    def test_attractions_and_packages_staff_permission(self):
        # Create non-staff user
        self.client.login(username='traveller1', password='password123')

        # Test Attraction write fails for non-staff
        url = reverse('attraction-list')
        data = {
            'attraction_name': 'Baga Beach Watersports',
            'destination': self.destination.destination_id,
            'category': 'Adventure',
            'description': 'Fun water sports activities.',
            'entry_fee': '500.00',
            'opening_time': '09:00:00',
            'closing_time': '18:00:00',
            'average_visit_time': 120
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Test Package write fails for non-staff
        url2 = reverse('package-list')
        data2 = {
            'package_name': 'Goa Honeymoon Special',
            'destination': self.destination.destination_id,
            'duration': 5,
            'package_type': 'Couple',
            'price': '25000.00',
            'description': 'Romantic resort stay.'
        }
        response2 = self.client.post(url2, data2, format='json')
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

        # Create staff user
        staff_user = User.objects.create_superuser(username='staffadmin2', password='password123', email='admin2@test.com')
        self.client.login(username='staffadmin2', password='password123')

        # Staff can write Attraction
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Staff can write Package
        response2 = self.client.post(url2, data2, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

    def test_attraction_and_package_filtering(self):
        # Create destinations
        destination2 = Destination.objects.create(
            destination_name="Jaipur Heritage",
            city="Jaipur",
            state="Rajasthan",
            category="Heritage",
            description="Historic pink city.",
            best_season="Winter",
            ideal_days=3,
            budget_level="Moderate",
            average_cost_per_day=4000.00
        )

        # Create attractions for self.destination (Goa Beach)
        Attraction.objects.create(
            attraction_name="Calangute Watersports",
            destination=self.destination,
            category="Adventure",
            description="Water activities.",
            entry_fee=350.00,
            opening_time="09:00:00",
            closing_time="17:00:00",
            average_visit_time=90
        )
        # Create attraction for destination2 (Jaipur)
        Attraction.objects.create(
            attraction_name="Amber Fort Ride",
            destination=destination2,
            category="Heritage",
            description="Ride to fort.",
            entry_fee=200.00,
            opening_time="08:00:00",
            closing_time="18:00:00",
            average_visit_time=120
        )

        # Create package for Goa
        Package.objects.create(
            package_name="Goa Weekend Getaway",
            destination=self.destination,
            duration=3,
            package_type="Solo",
            price=8000.00,
            description="Short weekend beach stay."
        )
        # Create package for Jaipur
        Package.objects.create(
            package_name="Jaipur Royal Forts",
            destination=destination2,
            duration=4,
            package_type="Family",
            price=15000.00,
            description="Palace tour."
        )

        # Test Attraction destination filter
        url = reverse('attraction-list')
        response = self.client.get(url + f'?destination={self.destination.destination_id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['attraction_name'], 'Calangute Watersports')

        # Test Package destination filter
        url2 = reverse('package-list')
        response2 = self.client.get(url2 + f'?destination={destination2.destination_id}')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data['results']), 1)
        self.assertEqual(response2.data['results'][0]['package_name'], 'Jaipur Royal Forts')

    def test_unauthorized_error_response_format(self):
        # Accessing protected write endpoint without authentication
        url = reverse('trip-list')
        data = {
            'destination': self.destination.destination_id,
            'start_date': '2026-10-10',
            'end_date': '2026-10-12',
            'number_of_travelers': 2,
            'budget': '15000.00',
            'travel_type': 'Couple'
        }
        self.client.logout()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_api_docs_page(self):
        url = reverse('api-docs')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/docs.html')

    def test_seasons_staff_permission(self):
        # Create non-staff user
        self.client.login(username='traveller1', password='password123')

        url = reverse('season-list')
        data = {
            'destination': self.destination.destination_id,
            'season': 'Monsoon',
            'peak_months': 'July - Sept',
            'average_temperature': '25-30 C',
            'rainfall': 'Heavy',
            'travel_tip': 'Carry umbrellas.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Create staff user
        staff_user = User.objects.create_superuser(username='staffadmin3', password='password123', email='admin3@test.com')
        self.client.login(username='staffadmin3', password='password123')

        # Staff can write BestSeason
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_seasons_filtering_and_public_read(self):
        # Create multiple BestSeason records
        BestSeason.objects.create(
            destination=self.destination,
            season="Summer",
            peak_months="March - May",
            average_temperature="30-35 C",
            rainfall="Low",
            travel_tip="Wear cotton clothes."
        )

        destination2 = Destination.objects.create(
            destination_name="Ooty Hills",
            city="Ooty",
            state="Tamil Nadu",
            category="Hill Station",
            description="Beautiful tea gardens.",
            best_season="Summer",
            ideal_days=3,
            budget_level="Moderate",
            average_cost_per_day=3000.00
        )
        BestSeason.objects.create(
            destination=destination2,
            season="Winter",
            peak_months="Nov - Jan",
            average_temperature="10-15 C",
            rainfall="Low",
            travel_tip="Carry heavy woollens."
        )

        url = reverse('season-list')

        # Public list read works
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertTrue(len(results) >= 2)

        # Filter by destination
        response = self.client.get(url + f'?destination={destination2.destination_id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['season'], 'Winter')
