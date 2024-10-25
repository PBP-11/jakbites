from django.test import TestCase, Client
from django.contrib.auth.models import User
from main.models import Food, Restaurant, Client as ClientProfile

class ProfileViewTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.force_login(self.user)
        
        self.client_profile = ClientProfile.objects.create(user=self.user)

        self.restaurant = Restaurant.objects.create(name='Resto A')

        self.food = Food.objects.create(name='Nasi Goreng', price=10000, restaurant=self.restaurant)

        self.client_profile.favorite_foods.add(self.food)
        self.client_profile.favorite_restaurants.add(self.restaurant)


    def test_profile_view(self):
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 404)

    def test_change_username(self):
        response = self.client.post('/change-name/', {'new_value': 'testuser'})
        self.assertEqual(response.status_code, 404)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'testuser')

    def test_change_description(self):
        response = self.client.post('/change-description/', {'new_value': 'New Description'})
        self.assertEqual(response.status_code, 404)
        self.client_profile.refresh_from_db()
        self.assertEqual(self.client_profile.description, None)

    def test_upload_profile_picture(self):
        with open('test_image.jpg', 'wb') as f:
            f.write(b'Test Image Content')
        with open('test_image.jpg', 'rb') as f:
            response = self.client.post('/upload-profile-picture/', {'profile_picture': f})
            self.assertEqual(response.status_code, 404)

    def test_change_password(self):
        response = self.client.post('/change-password/', {
            'current_password': 'testpassword',
            'new_password': 'newpassword123'
        })
        self.assertEqual(response.status_code, 404)

    def test_toggle_resto_fav(self):
        response = self.client.post('/toggle-resto-fav/', content_type='application/json', data='{"selected_items": [%d]}' % self.restaurant.id)
        self.assertEqual(response.status_code, 404)

    def test_toggle_food_fav(self):
        response = self.client.post('/toggle-food-fav/', content_type='application/json', data='{"selected_items": [%d]}' % self.food.id)
        self.assertEqual(response.status_code, 404)