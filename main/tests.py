from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client as TestClient
from authentication.forms import ClientRegistrationForm
from main.models import Client

# Create your tests here.
class AuthenticationTests(TestCase):

    def setUp(self):
        self.client = TestClient()
        self.register_url = reverse('authentication:register')
        self.login_url = reverse('authentication:user_login')

    def test_register_view(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = ClientRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_registration(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(self.register_url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(Client.objects.filter(user__username='testuser').exists())

    def test_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_user_login(self):
        user = User.objects.create_user(username='testuser', password='testpassword123')
        Client.objects.create(user=user)
        login_data = {
            'username': 'testuser',
            'password': 'testpassword123',
        }
        response = self.client.post(self.login_url, data=login_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:show_att'))