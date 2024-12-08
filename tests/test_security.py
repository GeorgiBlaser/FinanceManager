from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class SecurityTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_protected_view_redirects_unauthenticated(self):
        response = self.client.get(reverse('profile'))  # Profile page
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")

    def test_protected_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200, msg="Authenticated user should access profile page.")

    def test_superuser_only_view(self):
        response = self.client.get('/admin/')  # Trying to access admin without login
        self.assertRedirects(response, '/admin/login/?next=/admin/',
                             msg_prefix="Admin panel should redirect to admin login.")

