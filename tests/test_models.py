from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Post, Category, Transaction


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author.username, 'testuser')
        self.assertTrue(isinstance(self.post, Post))
        self.assertEqual(str(self.post), 'Test Post')
