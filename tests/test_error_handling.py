from django.test import TestCase
from django.core.exceptions import PermissionDenied


class ErrorHandlingTests(TestCase):

    def test_404_error_page(self):
        response = self.client.get('/non-existent-url/')
        self.assertEqual(response.status_code, 404, msg="Non-existent URL should return a 404 status.")

    def test_403_error_page(self):
        response = self.client.get('/budgets/')
        self.assertEqual(response.status_code, 302, msg="Accessing protected URL should redirect to login.")
        self.assertIn('/login', response.url, msg="Redirect should go to login page.")
