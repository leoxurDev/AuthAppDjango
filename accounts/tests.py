from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import Profile

class ProfileAppTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a regular user and a staff user
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.staff_user = User.objects.create_user(username='staffuser', email='staff@example.com', password='staffpassword', is_staff=True)
        
    def test_home_page_renders_successfully(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Craft Your Beautiful Public Profile")

    def test_dashboard_redirects_unauthenticated_user(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_dashboard_renders_for_logged_in_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Customize Profile")
        
    def test_profile_view_displays_correctly(self):
        response = self.client.get(reverse('profile_view', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")
        
    def test_admin_dashboard_denied_for_regular_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_admin_dashboard_allowed_for_staff_user(self):
        self.client.login(username='staffuser', password='staffpassword')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Access Control Management")

    def test_private_profile_hidden_on_landing_page(self):
        profile = self.user.profile
        profile.is_private = True
        profile.save()
        
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'href="/profile/testuser/"')

    def test_owner_can_view_own_private_profile(self):
        profile = self.user.profile
        profile.is_private = True
        profile.save()
        
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile_view', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Preview Mode: Your profile is currently set to Private")

    def test_anonymous_visitor_sees_lock_screen_for_private_profile(self):
        profile = self.user.profile
        profile.is_private = True
        profile.save()
        
        response = self.client.get(reverse('profile_view', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Private Portfolio")
        self.assertContains(response, "is currently set to private")
