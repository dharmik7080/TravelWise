from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Destination

class DestinationCRUDTests(TestCase):
    def setUp(self):
        self.username = "traveller"
        self.password = "Secr3tP@ssw0rd!"
        self.user = User.objects.create_user(
            username=self.username,
            email="traveller@example.com",
            password=self.password
        )
        self.dest = Destination.objects.create(
            destination_name="Grand Canyon",
            city="Tusayan",
            state="Arizona",
            region="West",
            category="Nature",
            description="Deep canyon carved by the Colorado River.",
            best_season="Spring",
            ideal_days=3,
            budget_level="Moderate",
            average_cost_per_day=150.00,
            average_rating=4.8
        )

    def test_destination_list_view_publicly_accessible(self):
        # List is viewable by anyone
        response = self.client.get(reverse('destinations:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'destinations/destination_list.html')
        self.assertContains(response, "Grand Canyon")

    def test_destination_list_pagination(self):
        # Create 9 more destinations (total 10)
        for i in range(9):
            Destination.objects.create(
                destination_name=f"Spot {i}",
                city="TestCity",
                category="Nature",
                description="Overview description",
                best_season="Summer",
                budget_level="Moderate",
                average_cost_per_day=100.00
            )
        response = self.client.get(reverse('destinations:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['destinations']), 9)
        
        # Go to page 2 and verify remaining destination is listed
        response_page2 = self.client.get(reverse('destinations:list') + '?page=2')
        self.assertEqual(response_page2.status_code, 200)
        self.assertEqual(len(response_page2.context['destinations']), 1)

    def test_destination_search_by_name(self):
        response = self.client.get(reverse('destinations:list') + '?q=canyon')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Grand Canyon")
        self.assertEqual(len(response.context['destinations']), 1)

    def test_destination_search_by_city(self):
        response = self.client.get(reverse('destinations:list') + '?q=tusayan')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Grand Canyon")
        self.assertEqual(len(response.context['destinations']), 1)

    def test_destination_search_by_state(self):
        response = self.client.get(reverse('destinations:list') + '?q=ARIZONA')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Grand Canyon")

    def test_destination_search_no_results(self):
        response = self.client.get(reverse('destinations:list') + '?q=Atlantis')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Destinations Found")
        self.assertEqual(len(response.context['destinations']), 0)

    def test_destination_filter_by_state(self):
        response = self.client.get(reverse('destinations:list') + '?state=Arizona')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Grand Canyon")
        
        response_empty = self.client.get(reverse('destinations:list') + '?state=California')
        self.assertEqual(response_empty.status_code, 200)
        self.assertEqual(len(response_empty.context['destinations']), 0)

    def test_destination_filter_by_category(self):
        response = self.client.get(reverse('destinations:list') + '?category=Nature')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Grand Canyon")

    def test_destination_filter_multiple_simultaneously(self):
        Destination.objects.create(
            destination_name="Kyoto",
            city="Kyoto",
            category="Cultural",
            description="Historical temples.",
            best_season="Autumn",
            budget_level="Moderate",
            average_cost_per_day=200.00
        )
        response = self.client.get(reverse('destinations:list') + '?category=Nature&budget_level=Moderate')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['destinations']), 1)
        self.assertContains(response, "Grand Canyon")

    def test_destination_sort_by_rating(self):
        Destination.objects.create(
            destination_name="Highest Rated Kyoto",
            city="Kyoto",
            category="Cultural",
            description="Beautiful city.",
            best_season="Spring",
            budget_level="Moderate",
            average_cost_per_day=180.00,
            average_rating=4.9
        )
        response = self.client.get(reverse('destinations:list') + '?sort_by=rating')
        self.assertEqual(response.status_code, 200)
        destinations = list(response.context['destinations'])
        self.assertEqual(destinations[0].destination_name, "Highest Rated Kyoto")
        self.assertEqual(destinations[1].destination_name, "Grand Canyon")

    def test_destination_sort_by_cost(self):
        Destination.objects.create(
            destination_name="Cheaper Spot",
            city="Cheaper",
            category="Nature",
            description="Cheap nature hike.",
            best_season="Spring",
            budget_level="Budget",
            average_cost_per_day=50.00
        )
        response = self.client.get(reverse('destinations:list') + '?sort_by=cost')
        self.assertEqual(response.status_code, 200)
        destinations = list(response.context['destinations'])
        self.assertEqual(destinations[0].destination_name, "Cheaper Spot")

    def test_home_page_featured_destinations(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, "Grand Canyon")
        self.assertEqual(len(response.context['featured_destinations']), 1)

    def test_destination_detail_view_publicly_accessible(self):
        # Details viewable by anyone
        response = self.client.get(reverse('destinations:detail', kwargs={'pk': self.dest.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'destinations/destination_detail.html')
        self.assertContains(response, "Deep canyon carved")

    def test_destination_create_login_required(self):
        # Block anonymous creation
        response = self.client.get(reverse('destinations:create'))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('destinations:create')}")

    def test_destination_create_authenticated(self):
        # Allow logged in creation
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('destinations:create'), {
            'destination_name': 'Kyoto',
            'city': 'Kyoto',
            'state': '',
            'region': 'Kansai',
            'category': 'Cultural',
            'description': 'Famous historical temples and gardens.',
            'best_season': 'Autumn',
            'ideal_days': 4,
            'budget_level': 'Moderate',
            'average_cost_per_day': 200.00,
            'average_rating': 4.9,
            'family_friendly': True,
            'couple_friendly': True,
            'solo_friendly': True
        })
        self.assertRedirects(response, reverse('destinations:list'))
        self.assertTrue(Destination.objects.filter(destination_name='Kyoto').exists())

    def test_destination_update_login_required(self):
        # Block anonymous edits
        response = self.client.get(reverse('destinations:update', kwargs={'pk': self.dest.pk}))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('destinations:update', kwargs={'pk': self.dest.pk})}")

    def test_destination_update_authenticated(self):
        # Allow logged in updates
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('destinations:update', kwargs={'pk': self.dest.pk}), {
            'destination_name': 'Grand Canyon National Park',
            'city': 'Tusayan',
            'state': 'Arizona',
            'region': 'West',
            'category': 'Nature',
            'description': 'Extensive overview description.',
            'best_season': 'Spring',
            'ideal_days': 4,
            'budget_level': 'Moderate',
            'average_cost_per_day': 160.00,
            'average_rating': 4.9,
            'family_friendly': True,
            'couple_friendly': True,
            'solo_friendly': True
        })
        self.assertRedirects(response, reverse('destinations:detail', kwargs={'pk': self.dest.pk}))
        self.dest.refresh_from_db()
        self.assertEqual(self.dest.destination_name, 'Grand Canyon National Park')
        self.assertEqual(self.dest.ideal_days, 4)

    def test_destination_delete_login_required(self):
        # Block anonymous deletion
        response = self.client.post(reverse('destinations:delete', kwargs={'pk': self.dest.pk}))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('destinations:delete', kwargs={'pk': self.dest.pk})}")

    def test_destination_delete_authenticated(self):
        # Allow logged in deletes
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('destinations:delete', kwargs={'pk': self.dest.pk}))
        self.assertRedirects(response, reverse('destinations:list'))
        self.assertFalse(Destination.objects.filter(pk=self.dest.pk).exists())


class ImportDestinationsCommandTests(TestCase):
    def setUp(self):
        import tempfile
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_import_destinations_command_success(self):
        import csv
        import os
        from django.core.management import call_command
        
        csv_path = os.path.join(self.temp_dir.name, "import.csv")
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'destination_name', 'city', 'state', 'region', 'category',
                'description', 'best_season', 'ideal_days', 'budget_level',
                'average_cost_per_day', 'family_friendly', 'couple_friendly',
                'solo_friendly', 'average_rating'
            ])
            writer.writerow([
                'Kyoto', 'Kyoto', 'Kansai', 'Japan', 'Cultural',
                'Famous historic temples.', 'Autumn', 4, 'Moderate',
                200.00, True, True, True, 4.9
            ])
            writer.writerow([
                'Mount Fuji', 'Shizuoka', '', 'Japan', 'Nature',
                'Highest peak in Japan.', 'Summer', 2, 'Budget',
                80.00, True, True, True, 4.8
            ])
        
        # Call the management command
        call_command('import_destinations', csv_path)
        
        # Verify both destinations were created
        self.assertEqual(Destination.objects.count(), 2)
        self.assertTrue(Destination.objects.filter(destination_name='Kyoto').exists())
        self.assertTrue(Destination.objects.filter(destination_name='Mount Fuji').exists())

    def test_import_destinations_command_ignores_duplicates_and_invalid(self):
        import csv
        import os
        from django.core.management import call_command

        # Create one pre-existing destination
        Destination.objects.create(
            destination_name="Kyoto",
            city="Kyoto",
            category="Cultural",
            description="Pre-existing",
            best_season="Autumn",
            budget_level="Moderate",
            average_cost_per_day=200.00
        )
        
        csv_path = os.path.join(self.temp_dir.name, "import_dup.csv")
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'destination_name', 'city', 'state', 'region', 'category',
                'description', 'best_season', 'ideal_days', 'budget_level',
                'average_cost_per_day', 'family_friendly', 'couple_friendly',
                'solo_friendly', 'average_rating'
            ])
            # Duplicate entry (should be skipped)
            writer.writerow([
                'Kyoto', 'Kyoto', 'Kansai', 'Japan', 'Cultural',
                'Famous historic temples.', 'Autumn', 4, 'Moderate',
                200.00, True, True, True, 4.9
            ])
            # Invalid entry missing city (should be skipped)
            writer.writerow([
                'Paris', '', 'IDF', 'Europe', 'Cultural',
                'Scenic city.', 'Spring', 3, 'Luxury',
                300.00, True, True, True, 4.7
            ])
            # Valid entry (should be imported)
            writer.writerow([
                'Mount Fuji', 'Shizuoka', '', 'Japan', 'Nature',
                'Highest peak in Japan.', 'Summer', 2, 'Budget',
                80.00, True, True, True, 4.8
            ])
            
        call_command('import_destinations', csv_path)
        
        # Only Mount Fuji and original Kyoto should exist (total 2)
        self.assertEqual(Destination.objects.count(), 2)
        self.assertTrue(Destination.objects.filter(destination_name='Mount Fuji').exists())

    def test_import_destinations_command_invalid_path(self):
        from django.core.management import call_command
        from django.core.management.base import CommandError
        with self.assertRaises(CommandError):
            call_command('import_destinations', 'non_existent_file.csv')

    def test_get_current_weather_success(self):
        import json
        from unittest.mock import patch, MagicMock
        from .weather_service import get_current_weather
        
        mock_response_data = {
            'main': {'temp': 24.3, 'humidity': 60},
            'weather': [{'main': 'Clear', 'icon': '01d'}],
            'wind': {'speed': 4.5}
        }
        
        with patch('urllib.request.urlopen') as mock_urlopen, \
             patch('django.conf.settings.OPENWEATHER_API_KEY', 'valid_test_key'):
            mock_response = MagicMock()
            mock_response.status = 200
            mock_response.read.return_value = json.dumps(mock_response_data).encode('utf-8')
            mock_urlopen.return_value.__enter__.return_value = mock_response
            
            weather = get_current_weather("Tusayan")
            self.assertIsNotNone(weather)
            self.assertEqual(weather['temp'], 24)
            self.assertEqual(weather['condition'], 'Clear')
            self.assertEqual(weather['humidity'], 60)
            self.assertEqual(weather['wind_speed'], 4.5)
            self.assertEqual(weather['icon'], '01d')

    def test_get_current_weather_api_failure_graceful(self):
        from unittest.mock import patch
        from .weather_service import get_current_weather
        
        with patch('urllib.request.urlopen', side_effect=Exception("API offline")), \
             patch('django.conf.settings.OPENWEATHER_API_KEY', 'valid_test_key'):
            weather = get_current_weather("Tusayan")
            self.assertIsNone(weather)


class DestinationAdminTests(TestCase):
    def setUp(self):
        self.username = "admin"
        self.password = "adminpass"
        self.admin_user = User.objects.create_superuser(
            username=self.username,
            email="admin@example.com",
            password=self.password
        )
        self.dest = Destination.objects.create(
            destination_name="Grand Canyon Admin",
            city="Tusayan",
            state="Arizona",
            category="Nature",
            description="Deep canyon.",
            best_season="Spring",
            ideal_days=3,
            budget_level="Moderate",
            average_cost_per_day=150.00,
            average_rating=4.8
        )

    def test_destination_admin_list_display_and_features(self):
        from django.contrib.admin.sites import site
        from .admin import DestinationAdmin
        
        # Verify class registration
        self.assertIn(Destination, site._registry)
        admin_instance = site._registry[Destination]
        self.assertIsInstance(admin_instance, DestinationAdmin)
        
        # Verify display columns config matches requirements
        expected_list_display = ('image_preview', 'destination_name', 'state', 'category', 'budget_level', 'best_season', 'average_rating')
        self.assertEqual(admin_instance.list_display, expected_list_display)
        
        # Verify search fields configuration
        expected_search_fields = ('destination_name', 'city')
        self.assertEqual(admin_instance.search_fields, expected_search_fields)
        
        # Verify list filters configuration
        expected_list_filter = ('state', 'category', 'budget_level')
        self.assertEqual(admin_instance.list_filter, expected_list_filter)
        
        # Verify ordering configuration
        self.assertEqual(admin_instance.ordering, ('destination_name',))
        
        # Verify pagination limit
        self.assertEqual(admin_instance.list_per_page, 20)

    def test_destination_admin_image_preview_generation(self):
        from django.contrib.admin.sites import site
        admin_instance = site._registry[Destination]
        
        # Test image_preview returns "No Image" when field is empty
        preview_html = admin_instance.image_preview(self.dest)
        self.assertIn("No Image", preview_html)
        
        # Test image_preview_form returns placeholder string when field is empty
        preview_form_html = admin_instance.image_preview_form(self.dest)
        self.assertIn("No image uploaded yet.", preview_form_html)


class DestinationCSVExportTests(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User
        self.username = "admin"
        self.password = "adminpass"
        self.admin_user = User.objects.create_superuser(
            username=self.username,
            email="admin@example.com",
            password=self.password
        )
        self.dest = Destination.objects.create(
            destination_name="Grand Canyon Export",
            city="Tusayan",
            state="Arizona",
            category="Nature",
            description="Deep canyon.",
            best_season="Spring",
            ideal_days=3,
            budget_level="Moderate",
            average_cost_per_day=150.00,
            average_rating=4.8
        )

    def test_destination_csv_export_requires_staff(self):
        # Unauthenticated redirects to admin login
        response = self.client.get('/admin/destinations/destination/export-csv/')
        self.assertEqual(response.status_code, 302)

        # Non-staff user redirects to admin login
        from django.contrib.auth.models import User
        User.objects.create_user(username="simple_user", password="simple_password")
        self.client.login(username="simple_user", password="simple_password")
        response = self.client.get('/admin/destinations/destination/export-csv/')
        self.assertEqual(response.status_code, 302)

    def test_destination_csv_export_success(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/admin/destinations/destination/export-csv/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('attachment; filename="destinations.csv"', response['Content-Disposition'])
        
        content = b"".join(response.streaming_content).decode('utf-8')
        self.assertIn("destination_name", content)
        self.assertIn("Grand Canyon Export", content)
        self.assertIn("Arizona", content)


class DestinationModelValidationTests(TestCase):
    def test_destination_validation_invalid_rating(self):
        from django.core.exceptions import ValidationError
        dest = Destination(
            destination_name="Invalid Rating Dest",
            city="City",
            category="Nature",
            description="Desc",
            best_season="Summer",
            budget_level="Moderate",
            average_cost_per_day=100.00,
            average_rating=6.0  # Invalid rating
        )
        with self.assertRaises(ValidationError):
            dest.clean()

    def test_destination_validation_negative_cost(self):
        from django.core.exceptions import ValidationError
        dest = Destination(
            destination_name="Negative Cost Dest",
            city="City",
            category="Nature",
            description="Desc",
            best_season="Summer",
            budget_level="Moderate",
            average_cost_per_day=-50.00,  # Negative cost
            average_rating=4.5
        )
        with self.assertRaises(ValidationError):
            dest.clean()

    def test_destination_validation_invalid_ideal_days(self):
        from django.core.exceptions import ValidationError
        dest = Destination(
            destination_name="Invalid Days Dest",
            city="City",
            category="Nature",
            description="Desc",
            best_season="Summer",
            budget_level="Moderate",
            average_cost_per_day=100.00,
            ideal_days=0,  # Zero or negative
            average_rating=4.5
        )
        with self.assertRaises(ValidationError):
            dest.clean()


