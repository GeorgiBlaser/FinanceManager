from django.test import TestCase
from core.forms import CreatePostForm, ContactForm


class FormTests(TestCase):

    def test_create_post_form_valid(self):
        form_data = {'title': 'Test Post', 'content': 'This is a test post.'}
        form = CreatePostForm(data=form_data)
        self.assertTrue(form.is_valid(), msg="CreatePostForm should be valid with correct data.")

    def test_create_post_form_invalid(self):
        form_data = {'title': '', 'content': 'This is a test post.'}
        form = CreatePostForm(data=form_data)
        self.assertFalse(form.is_valid(), msg="CreatePostForm should be invalid without a title.")

    def test_contact_form_valid(self):
        form_data = {'name': 'John Doe', 'email': 'john.doe@example.com', 'message': 'Hello!'}
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid(), msg="ContactForm should be valid with correct data.")

    def test_contact_form_invalid_email(self):
        form_data = {'name': 'John Doe', 'email': 'invalid-email', 'message': 'Hello!'}
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid(), msg="ContactForm should be invalid with incorrect email.")
