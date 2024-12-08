from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase


class AuthenticationTests(TestCase):

    def setUp(self):
        # Създаване на потребител
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_register_view(self):
        """Проверка дали регистрацията работи правилно."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

        # Регистрация на нов потребител
        data = {
            'username': 'newuser',
            'password': 'securepassword',  # Правилно поле за парола
            'confirm_password': 'securepassword',  # Поле за потвърждение на паролата
            'email': 'newuser@example.com'  # Ако формата изисква email
        }
        response = self.client.post(reverse('register'), data)

        # Диагностика - отпечатване на грешки, ако има такива
        if response.status_code == 200 and 'form' in response.context:
            print("Форма грешки:", response.context['form'].errors)

        self.assertEqual(response.status_code, 302)  # Пренасочване след успешна регистрация
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view(self):
        """Проверка дали потребителят може да влезе успешно."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        # Вход в системата
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 302)  # Пренасочване след вход
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_logout_view(self):
        """Проверка дали излизането изчиства сесията."""
        # Логваме се
        self.client.login(username='testuser', password='password123')

        # Излизане от системата
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Пренасочване след излизане
        self.assertFalse('_auth_user_id' in self.client.session)
