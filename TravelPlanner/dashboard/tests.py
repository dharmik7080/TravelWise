from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

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
