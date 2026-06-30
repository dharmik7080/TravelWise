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
