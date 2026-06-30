from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthenticationTests(TestCase):
    def setUp(self):
        # Create a default user for testing login & duplicates
        self.username = "testuser"
        self.email = "testuser@example.com"
        self.password = "Secr3tP@ssw0rd!"
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

    def test_pages_access(self):
        # Test that registration and login pages load successfully
        response_register = self.client.get(reverse('accounts:register'))
        self.assertEqual(response_register.status_code, 200)
        self.assertTemplateUsed(response_register, 'accounts/register.html')

        response_login = self.client.get(reverse('accounts:login'))
        self.assertEqual(response_login.status_code, 200)
        self.assertTemplateUsed(response_login, 'accounts/login.html')

    def test_successful_registration(self):
        # Test registering a new user successfully
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'NewS3cretP@ss!',
            'password2': 'NewS3cretP@ss!'
        })
        # Check redirection to login page
        self.assertRedirects(response, reverse('accounts:login'))
        # Check database entry
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_duplicate_email_registration(self):
        # Test registering with an email that already exists
        response = self.client.post(reverse('accounts:register'), {
            'username': 'uniqueusername',
            'email': self.email,  # duplicate email
            'password1': 'NewS3cretP@ss!',
            'password2': 'NewS3cretP@ss!'
        })
        self.assertEqual(response.status_code, 200)
        # Form should have errors
        form = response.context['form']
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'][0], "A user with this email address already exists.")

    def test_duplicate_username_registration(self):
        # Test registering with a username that already exists
        response = self.client.post(reverse('accounts:register'), {
            'username': self.username,  # duplicate username
            'email': 'uniqueemail@example.com',
            'password1': 'NewS3cretP@ss!',
            'password2': 'NewS3cretP@ss!'
        })
        self.assertEqual(response.status_code, 200)
        # Form should have errors
        form = response.context['form']
        self.assertIn('username', form.errors)

    def test_weak_password_registration(self):
        # Test registration with a weak password (too short/simple)
        response = self.client.post(reverse('accounts:register'), {
            'username': 'anotheruser',
            'email': 'another@example.com',
            'password1': '123',  # weak password
            'password2': '123'
        })
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertIn('password1', form.errors)

    def test_login_and_redirect(self):
        # Test login redirects to dashboard
        response = self.client.post(reverse('accounts:login'), {
            'username': self.username,
            'password': self.password
        })
        # login redirects to LOGIN_REDIRECT_URL (dashboard:index)
        self.assertRedirects(response, reverse('dashboard:index'))

    def test_login_invalid_credentials(self):
        # Test login fails with wrong credentials
        response = self.client.post(reverse('accounts:login'), {
            'username': self.username,
            'password': 'WrongPassword123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_logout_redirect(self):
        # Log in first
        self.client.login(username=self.username, password=self.password)
        # Logout is POST in Django 5.x
        response = self.client.post(reverse('accounts:logout'))
        # Should redirect to home
        self.assertRedirects(response, reverse('home'))

    def test_profile_page_login_required(self):
        # Unauthenticated users should be redirected to login page
        response = self.client.get(reverse('accounts:profile'))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('accounts:profile')}")

    def test_profile_page_loads(self):
        # Authenticated user should see profile page
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertContains(response, self.username)

    def test_profile_update_successful(self):
        # Authenticated user updates profile successfully
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('accounts:profile'), {
            'first_name': 'NewFirst',
            'last_name': 'NewLast',
            'email': 'newemail@example.com'
        })
        self.assertRedirects(response, reverse('accounts:profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'NewFirst')
        self.assertEqual(self.user.last_name, 'NewLast')
        self.assertEqual(self.user.email, 'newemail@example.com')

    def test_profile_update_duplicate_email(self):
        # Try updating email to one that belongs to another user
        User.objects.create_user(username="otheruser", email="other@example.com", password="password123")
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('accounts:profile'), {
            'first_name': 'NewFirst',
            'last_name': 'NewLast',
            'email': 'other@example.com'
        })
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'][0], "A user with this email address already exists.")

    def test_profile_update_same_email_is_allowed(self):
        # Updating other profile details while keeping same email is allowed
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('accounts:profile'), {
            'first_name': 'UpdatedFirst',
            'last_name': 'UpdatedLast',
            'email': self.email  # Keep original email
        })
        self.assertRedirects(response, reverse('accounts:profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'UpdatedFirst')
        self.assertEqual(self.user.email, self.email)

    def test_password_change_login_required(self):
        # Unauthenticated user redirected to login
        response = self.client.get(reverse('accounts:password_change'))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('accounts:password_change')}")

    def test_password_change_page_loads(self):
        # Authenticated user should load change password form
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('accounts:password_change'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_change.html')

    def test_password_change_successful(self):
        # Success path updates password and keeps user logged in
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('accounts:password_change'), {
            'old_password': self.password,
            'old_password_input': self.password, # Django names fields in PasswordChangeForm: old_password, old_password_input
            'new_password1': 'NewS3cretP@ss!',
            'new_password2': 'NewS3cretP@ss!'
        })
        self.assertRedirects(response, reverse('accounts:profile'))
        # Check that user remains authenticated after redirection
        # By calling a login-required page and ensuring it doesn't redirect
        profile_response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(profile_response.status_code, 200)

    def test_password_change_invalid(self):
        # Fail path with mismatched confirm password
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('accounts:password_change'), {
            'old_password': self.password,
            'new_password1': 'NewS3cretP@ss!',
            'new_password2': 'Mismatch123!'
        })
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertIn('new_password2', form.errors)

    def test_password_reset_page_loads(self):
        response = self.client.get(reverse('accounts:password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset.html')

    def test_password_reset_email_sent(self):
        from django.core import mail
        response = self.client.post(reverse('accounts:password_reset'), {
            'email': self.email
        })
        self.assertRedirects(response, reverse('accounts:password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Password reset request", mail.outbox[0].subject)
        self.assertIn(self.username, mail.outbox[0].body)
