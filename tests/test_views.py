from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Post


class ViewTests(TestCase):

    def setUp(self):
        # Създаване на потребител
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

        # Създаване на тестов пост
        self.post = Post.objects.create(
            title="Test Post",
            content="Test Content",
            author=self.user
        )

    def test_home_page_view(self):
        """Проверка дали началната страница се зарежда правилно."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_post_list_view(self):
        """Проверка дали списъкът с постове е достъпен."""
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_list.html')
        self.assertContains(response, self.post.title)

    def test_post_detail_view(self):
        """Проверка дали детайлите на поста се зареждат правилно."""
        response = self.client.get(reverse('post_detail', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_detail.html')
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)


class PostActionsTests(TestCase):

    def setUp(self):
        # Създаване на потребител
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

        # Създаване на тестов пост
        self.post = Post.objects.create(
            title="Test Post",
            content="Test Content",
            author=self.user
        )

    def test_create_post_view(self):
        """Проверка дали формата за създаване на пост работи правилно."""
        response = self.client.get(reverse('create_post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_post.html')

        # Създаване на нов пост
        data = {'title': 'New Post', 'content': 'New Content'}
        response = self.client.post(reverse('create_post'), data)
        self.assertEqual(response.status_code, 302)  # Пренасочване след създаване
        self.assertTrue(Post.objects.filter(title='New Post').exists())

    def test_edit_post_view(self):
        """Проверка дали потребителят може да редактира пост."""
        response = self.client.get(reverse('update_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_post.html')

        # Редакция на поста
        data = {'title': 'Updated Post', 'content': 'Updated Content'}
        response = self.client.post(reverse('update_post', args=[self.post.id]), data)
        self.assertEqual(response.status_code, 302)  # Пренасочване след редакция
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Post')

    def test_delete_post_view(self):
        """Проверка дали постът може да бъде изтрит."""
        response = self.client.get(reverse('delete_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_post.html')

        # Изтриване на поста
        response = self.client.post(reverse('delete_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)  # Пренасочване след изтриване
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

