from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from destinations.models import Destination
from .models import Attraction

User = get_user_model()

class AttractionTests(TestCase):
    """
    Test suite for Tourist Attraction views, forms, models, and template integrations.
    """
    def setUp(self):
        self.username = "testuser"
        self.password = "Secr3tP@ssw0rd!"
        self.email = "testuser@example.com"
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email=self.email
        )
        self.destination = Destination.objects.create(
            destination_name="Grand Canyon National Park",
            city="Tusayan",
            state="Arizona",
            category="Nature",
            description="Deep canyon carved by the Colorado River.",
            best_season="Spring",
            ideal_days=2,
            budget_level="Moderate",
            average_cost_per_day=150.00,
            average_rating=4.8
        )
        self.attraction = Attraction.objects.create(
            attraction_name="Mather Point",
            destination=self.destination,
            category="Scenic Lookout",
            description="A popular canyon viewpoint.",
            entry_fee=0.00,
            opening_time="08:00:00",
            closing_time="18:00:00",
            average_visit_time=45
        )

    def test_attraction_list_view(self):
        response = self.client.get(reverse('attractions:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'attractions/attraction_list.html')
        self.assertContains(response, "Mather Point")

    def test_attraction_detail_view(self):
        response = self.client.get(reverse('attractions:detail', kwargs={'pk': self.attraction.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'attractions/attraction_detail.html')
        self.assertContains(response, "A popular canyon viewpoint")

    def test_attraction_create_anonymous_redirects(self):
        response = self.client.get(reverse('attractions:create'))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('attractions:create')}")

    def test_attraction_create_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        dummy_img = SimpleUploadedFile(
            name='test_img.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b',
            content_type='image/jpeg'
        )
        response = self.client.post(reverse('attractions:create'), {
            'attraction_name': 'Desert View Watchtower',
            'destination': self.destination.pk,
            'category': 'Architecture',
            'description': 'Historic stone tower.',
            'entry_fee': 5.00,
            'opening_time': '09:00',
            'closing_time': '17:00',
            'average_visit_time': 60,
            'image': dummy_img
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Attraction.objects.count(), 2)
        self.assertTrue(Attraction.objects.filter(attraction_name='Desert View Watchtower').exists())

    def test_attraction_update_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('attractions:update', kwargs={'pk': self.attraction.pk}), {
            'attraction_name': 'Mather Point (Updated)',
            'destination': self.destination.pk,
            'category': 'Scenic Lookout',
            'description': 'Canyon views.',
            'entry_fee': 0.00,
            'opening_time': '08:00',
            'closing_time': '18:00',
            'average_visit_time': 45
        })
        self.assertEqual(response.status_code, 302)
        self.attraction.refresh_from_db()
        self.assertEqual(self.attraction.attraction_name, 'Mather Point (Updated)')

    def test_attraction_delete_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('attractions:delete', kwargs={'pk': self.attraction.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Attraction.objects.count(), 0)

    def test_destination_details_shows_attractions(self):
        response = self.client.get(reverse('destinations:detail', kwargs={'pk': self.destination.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mather Point")

    def test_attraction_search_by_name(self):
        response = self.client.get(reverse('attractions:list') + '?q=mather')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mather Point")
        self.assertEqual(len(response.context['attractions']), 1)

    def test_attraction_filter_by_destination(self):
        response = self.client.get(reverse('attractions:list') + f'?destination={self.destination.pk}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mather Point")

    def test_attraction_filter_by_category(self):
        response = self.client.get(reverse('attractions:list') + '?category=Scenic+Lookout')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mather Point")

    def test_attraction_filter_by_entry_type_free(self):
        response = self.client.get(reverse('attractions:list') + '?entry_type=free')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mather Point")
        
    def test_attraction_filter_by_entry_type_paid(self):
        response = self.client.get(reverse('attractions:list') + '?entry_type=paid')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['attractions']), 0)
        self.assertContains(response, "No Attractions Found")


class AttractionAdminTests(TestCase):
    def setUp(self):
        self.username = "admin"
        self.password = "adminpass"
        self.admin_user = User.objects.create_superuser(
            username=self.username,
            email="admin@example.com",
            password=self.password
        )
        self.destination = Destination.objects.create(
            destination_name="Grand Canyon Admin View",
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
        self.attraction = Attraction.objects.create(
            attraction_name="Bright Angel Trail",
            destination=self.destination,
            category="Hiking",
            description="Scenic canyon descent.",
            entry_fee=0.00,
            opening_time="06:00:00",
            closing_time="19:00:00",
            average_visit_time=240
        )

    def test_attraction_admin_list_display_and_features(self):
        from django.contrib.admin.sites import site
        from .admin import AttractionAdmin
        
        self.assertIn(Attraction, site._registry)
        admin_instance = site._registry[Attraction]
        self.assertIsInstance(admin_instance, AttractionAdmin)
        
        expected_list_display = ('image_preview', 'attraction_name', 'destination', 'category', 'entry_fee', 'opening_time', 'closing_time')
        self.assertEqual(admin_instance.list_display, expected_list_display)
        
        expected_search_fields = ('attraction_name', 'destination__destination_name', 'category')
        self.assertEqual(admin_instance.search_fields, expected_search_fields)
        
        expected_list_filter = ('destination', 'category')
        self.assertEqual(admin_instance.list_filter, expected_list_filter)
        
        self.assertEqual(admin_instance.ordering, ('attraction_name',))
        self.assertEqual(admin_instance.list_per_page, 20)

    def test_attraction_admin_image_preview_generation(self):
        from django.contrib.admin.sites import site
        admin_instance = site._registry[Attraction]
        
        preview_html = admin_instance.image_preview(self.attraction)
        self.assertIn("No Image", preview_html)
        
        preview_form_html = admin_instance.image_preview_form(self.attraction)
        self.assertIn("No image uploaded yet.", preview_form_html)


class ImportAttractionsCommandTests(TestCase):
    def setUp(self):
        import tempfile
        self.temp_dir = tempfile.TemporaryDirectory()
        self.destination = Destination.objects.create(
            destination_name="Grand Canyon National Park",
            city="Tusayan",
            state="Arizona",
            category="Nature",
            description="Canyon",
            best_season="Spring",
            ideal_days=2,
            budget_level="Moderate",
            average_cost_per_day=150.00,
            average_rating=4.8
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_import_attractions_command_success(self):
        import csv
        import os
        from django.core.management import call_command
        
        csv_path = os.path.join(self.temp_dir.name, "import_attractions.csv")
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'attraction_name', 'destination_name', 'category', 
                'description', 'entry_fee', 'opening_time', 'closing_time', 'average_visit_time'
            ])
            writer.writerow([
                'Scenic Point', 'Grand Canyon National Park', 'Lookout',
                'Nice viewpoint.', 0.00, '08:00:00', '18:00:00', 45
            ])
            writer.writerow([
                'Hiking Trail', 'Grand Canyon National Park', 'Hiking',
                'Steep trail down.', 5.00, '06:00:00', '19:00:00', 120
            ])
        
        call_command('import_attractions', csv_path)
        self.assertEqual(Attraction.objects.count(), 2)
        self.assertTrue(Attraction.objects.filter(attraction_name='Scenic Point').exists())
        self.assertTrue(Attraction.objects.filter(attraction_name='Hiking Trail').exists())

    def test_import_attractions_command_invalid_path(self):
        from django.core.management import call_command
        from django.core.management.base import CommandError
        with self.assertRaises(CommandError):
            call_command('import_attractions', 'non_existent_attractions_file.csv')


class AttractionModelValidationTests(TestCase):
    def setUp(self):
        self.destination = Destination.objects.create(
            destination_name="Grand Canyon Validated",
            city="Tusayan",
            state="Arizona",
            category="Nature",
            description="Canyon",
            best_season="Spring",
            ideal_days=2,
            budget_level="Moderate",
            average_cost_per_day=150.00,
            average_rating=4.8
        )

    def test_attraction_validation_negative_fee(self):
        from django.core.exceptions import ValidationError
        attraction = Attraction(
            attraction_name="Negative Fee Attraction",
            destination=self.destination,
            category="Scenic Lookout",
            description="Viewpoint",
            entry_fee=-10.00,  # Negative entry fee
            opening_time="08:00:00",
            closing_time="18:00:00",
            average_visit_time=45
        )
        with self.assertRaises(ValidationError):
            attraction.clean()

    def test_attraction_validation_invalid_timing(self):
        from django.core.exceptions import ValidationError
        attraction = Attraction(
            attraction_name="Invalid Timing Attraction",
            destination=self.destination,
            category="Scenic Lookout",
            description="Viewpoint",
            entry_fee=0.00,
            opening_time="19:00:00",
            closing_time="08:00:00",  # Opening after closing
            average_visit_time=45
        )
        with self.assertRaises(ValidationError):
            attraction.clean()
