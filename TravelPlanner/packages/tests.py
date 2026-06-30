from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from destinations.models import Destination
from .models import Package

User = get_user_model()

class PackageTests(TestCase):
    """
    Test suite for travel package views, forms, models, and template integrations.
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
            destination_name="Yosemite National Park",
            city="Yosemite",
            state="California",
            category="Nature",
            description="Famous for giant ancient sequoia trees and waterfalls.",
            best_season="Summer",
            ideal_days=3,
            budget_level="Moderate",
            average_cost_per_day=200.00,
            average_rating=4.9
        )
        self.package = Package.objects.create(
            package_name="Yosemite Adventure Package",
            destination=self.destination,
            duration=3,
            package_type="Adventure",
            price=299.00,
            description="3 days hiking tour in Yosemite Valley."
        )

    def test_package_list_view(self):
        response = self.client.get(reverse('packages:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'packages/package_list.html')
        self.assertContains(response, "Yosemite Adventure Package")

    def test_package_detail_view(self):
        response = self.client.get(reverse('packages:detail', kwargs={'pk': self.package.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'packages/package_detail.html')
        self.assertContains(response, "3 days hiking tour in Yosemite Valley.")

    def test_package_create_anonymous_redirects(self):
        response = self.client.get(reverse('packages:create'))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('packages:create')}")

    def test_package_create_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        dummy_img = SimpleUploadedFile(
            name='package_img.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b',
            content_type='image/jpeg'
        )
        response = self.client.post(reverse('packages:create'), {
            'package_name': 'Yosemite Luxury Package',
            'destination': self.destination.pk,
            'duration': 5,
            'package_type': 'Luxury',
            'price': 999.00,
            'description': 'All inclusive luxury camping experience.',
            'image': dummy_img
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Package.objects.count(), 2)
        self.assertTrue(Package.objects.filter(package_name='Yosemite Luxury Package').exists())

    def test_package_update_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('packages:update', kwargs={'pk': self.package.pk}), {
            'package_name': 'Yosemite Adventure Package (Updated)',
            'destination': self.destination.pk,
            'duration': 4,
            'package_type': 'Adventure',
            'price': 349.00,
            'description': '4 days hiking tour in Yosemite Valley.'
        })
        self.assertEqual(response.status_code, 302)
        self.package.refresh_from_db()
        self.assertEqual(self.package.package_name, 'Yosemite Adventure Package (Updated)')
        self.assertEqual(self.package.duration, 4)

    def test_package_delete_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('packages:delete', kwargs={'pk': self.package.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Package.objects.count(), 0)

    def test_destination_details_shows_packages(self):
        response = self.client.get(reverse('destinations:detail', kwargs={'pk': self.destination.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Yosemite Adventure Package")


class PackageAdminTests(TestCase):
    def setUp(self):
        self.username = "admin"
        self.password = "adminpass"
        self.admin_user = User.objects.create_superuser(
            username=self.username,
            email="admin@example.com",
            password=self.password
        )
        self.destination = Destination.objects.create(
            destination_name="Yosemite National Park Admin",
            city="Yosemite",
            state="California",
            category="Nature",
            description="Giant sequoias.",
            best_season="Summer",
            ideal_days=3,
            budget_level="Moderate",
            average_cost_per_day=200.00,
            average_rating=4.9
        )
        self.package = Package.objects.create(
            package_name="Yosemite Hiking Tour",
            destination=self.destination,
            duration=3,
            package_type="Adventure",
            price=299.00,
            description="3 days hiking tour."
        )

    def test_package_admin_list_display_and_features(self):
        from django.contrib.admin.sites import site
        from .admin import PackageAdmin
        
        self.assertIn(Package, site._registry)
        admin_instance = site._registry[Package]
        self.assertIsInstance(admin_instance, PackageAdmin)
        
        expected_list_display = ('image_preview', 'package_name', 'destination', 'duration', 'package_type', 'price')
        self.assertEqual(admin_instance.list_display, expected_list_display)
        
        expected_search_fields = ('package_name', 'destination__destination_name')
        self.assertEqual(admin_instance.search_fields, expected_search_fields)
        
        expected_list_filter = ('destination', 'package_type')
        self.assertEqual(admin_instance.list_filter, expected_list_filter)
        
        self.assertEqual(admin_instance.ordering, ('price',))
        self.assertEqual(admin_instance.list_per_page, 20)

    def test_package_admin_image_preview_generation(self):
        from django.contrib.admin.sites import site
        admin_instance = site._registry[Package]
        
        preview_html = admin_instance.image_preview(self.package)
        self.assertIn("No Image", preview_html)
        
        preview_form_html = admin_instance.image_preview_form(self.package)
        self.assertIn("No image uploaded yet.", preview_form_html)


class ImportPackagesCommandTests(TestCase):
    def setUp(self):
        import tempfile
        self.temp_dir = tempfile.TemporaryDirectory()
        self.destination = Destination.objects.create(
            destination_name="Yosemite National Park",
            city="Yosemite",
            state="California",
            category="Nature",
            description="Park",
            best_season="Summer",
            ideal_days=3,
            budget_level="Moderate",
            average_cost_per_day=200.00,
            average_rating=4.9
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_import_packages_command_success(self):
        import csv
        import os
        from django.core.management import call_command
        
        csv_path = os.path.join(self.temp_dir.name, "import_packages.csv")
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'package_name', 'destination_name', 'duration', 
                'package_type', 'price', 'description'
            ])
            writer.writerow([
                'Budget Adventure', 'Yosemite National Park', 3,
                'Adventure', 199.00, '3 days tour.'
            ])
            writer.writerow([
                'Family Fun Tour', 'Yosemite National Park', 5,
                'Family', 499.00, '5 days family trip.'
            ])
        
        call_command('import_packages', csv_path)
        self.assertEqual(Package.objects.count(), 2)
        self.assertTrue(Package.objects.filter(package_name='Budget Adventure').exists())
        self.assertTrue(Package.objects.filter(package_name='Family Fun Tour').exists())

    def test_import_packages_command_invalid_path(self):
        from django.core.management import call_command
        from django.core.management.base import CommandError
        with self.assertRaises(CommandError):
            call_command('import_packages', 'non_existent_packages_file.csv')


class PackageCSVExportTests(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User
        self.username = "admin"
        self.password = "adminpass"
        self.admin_user = User.objects.create_superuser(
            username=self.username,
            email="admin@example.com",
            password=self.password
        )
        self.destination = Destination.objects.create(
            destination_name="Yosemite National Park Export",
            city="Yosemite",
            state="California",
            category="Nature",
            description="Giant sequoias.",
            best_season="Summer",
            ideal_days=3,
            budget_level="Moderate",
            average_cost_per_day=200.00,
            average_rating=4.9
        )
        self.package = Package.objects.create(
            package_name="Yosemite Hiking Tour Export",
            destination=self.destination,
            duration=3,
            package_type="Adventure",
            price=299.00,
            description="3 days hiking tour."
        )

    def test_package_csv_export_requires_staff(self):
        response = self.client.get('/admin/packages/package/export-csv/')
        self.assertEqual(response.status_code, 302)

    def test_package_csv_export_success(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/admin/packages/package/export-csv/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('attachment; filename="packages.csv"', response['Content-Disposition'])
        
        content = b"".join(response.streaming_content).decode('utf-8')
        self.assertIn("package_name", content)
        self.assertIn("destination__destination_name", content)
        self.assertIn("Yosemite Hiking Tour Export", content)
        self.assertIn("Yosemite National Park Export", content)
        self.assertIn("299.00", content)


class PackageModelValidationTests(TestCase):
    def setUp(self):
        self.destination = Destination.objects.create(
            destination_name="Yosemite National Park Validated",
            city="Yosemite",
            state="California",
            category="Nature",
            description="Park",
            best_season="Summer",
            ideal_days=3,
            budget_level="Moderate",
            average_cost_per_day=200.00,
            average_rating=4.9
        )

    def test_package_validation_negative_price(self):
        from django.core.exceptions import ValidationError
        package = Package(
            package_name="Negative Price Package",
            destination=self.destination,
            duration=3,
            package_type="Adventure",
            price=-100.00,  # Negative price
            description="Tour description"
        )
        with self.assertRaises(ValidationError):
            package.clean()

    def test_package_validation_invalid_duration(self):
        from django.core.exceptions import ValidationError
        package = Package(
            package_name="Invalid Duration Package",
            destination=self.destination,
            duration=0,  # Zero duration
            package_type="Adventure",
            price=299.00,
            description="Tour description"
        )
        with self.assertRaises(ValidationError):
            package.clean()
