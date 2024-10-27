from django.test import TestCase, Client
from django.contrib.auth.models import User
from main.models import Food, Restaurant, Client as ClientProfile
from user.forms import UserUpdateForm, ProfileUpdateForm
from django.core import serializers
from django.core.files.uploadedfile import SimpleUploadedFile
import json
from django.urls import reverse

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

    def test_profile_view_context(self):
        response = self.client.get(reverse('user:profile'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['user'], self.user)
        self.assertEqual(response.context['client'], self.client_profile)

        self.assertEqual(list(response.context['all_foods']), list(Food.objects.all()))
        self.assertEqual(list(response.context['all_restaurants']), list(Restaurant.objects.all()))

        self.assertEqual(list(response.context['favorite_foods']), list(self.client_profile.favorite_foods.all()))
        self.assertEqual(list(response.context['favorite_restaurants']), list(self.client_profile.favorite_restaurants.all()))

        self.assertJSONEqual(
            response.context['all_foods_json'],
            serializers.serialize('json', Food.objects.all())
        )
        self.assertJSONEqual(
            response.context['all_restaurants_json'],
            serializers.serialize('json', Restaurant.objects.all())
        )
        self.assertJSONEqual(
            response.context['favorite_foods_json'],
            serializers.serialize('json', self.client_profile.favorite_foods.all())
        )
        self.assertJSONEqual(
            response.context['favorite_restaurants_json'],
            serializers.serialize('json', self.client_profile.favorite_restaurants.all())
        )

        def test_upload_profile_picture_success(self):
            image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")

            response = self.client.post(reverse('user:upload_profile_picture'), {'profile_picture': image})

            self.assertRedirects(response, reverse('user:profile'))
            self.client_profile.refresh_from_db()
            self.assertIsNotNone(self.client_profile.profile_picture)

    def test_upload_profile_picture_no_profile(self):
        self.client_profile.delete()

        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")

        response = self.client.post(reverse('user:upload_profile_picture'), {'profile_picture': image})

        self.assertRedirects(response, reverse('user:profile'))
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any(m.message == 'User tidak memiliki profil yang terhubung.' for m in messages))


    def test_change_name_success(self):
        response = self.client.post(reverse('user:change_name'), {'new_value': 'newusername'})
        
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'message': 'Username updated successfully!'})

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')

    def test_change_name_empty(self):
        response = self.client.post(reverse('user:change_name'), {'new_value': ''})
        
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Username cannot be empty.'})
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'testuser')

    


class UserUpdateFormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')

    def test_user_update_form_valid_data(self):
        form_data = {
            'username': 'updateduser',
            'email': 'updateduser@example.com'
        }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_user_update_form_invalid_data(self):
        form_data = {
            'username': '',  
            'email': 'not-an-email' 
        }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)


class ProfileUpdateFormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
        self.client_profile = ClientProfile.objects.create(user=self.user)

    def test_profile_update_form_invalid_data(self):
        form_data = {
            'favorite_restaurants': '',  
            'favorite_foods': ''  
        }
        form = ProfileUpdateForm(data=form_data, instance=self.client_profile)
        self.assertFalse(form.is_valid())
        self.assertIn('favorite_restaurants', form.errors)
        self.assertIn('favorite_foods', form.errors)

class ToggleFoodFavViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.force_login(self.user)

        self.client_profile = ClientProfile.objects.create(user=self.user)

        self.restaurant = Restaurant.objects.create(name='Resto A')

        self.food1 = Food.objects.create(name='Nasi Goreng', price=10000, restaurant=self.restaurant)
        self.food2 = Food.objects.create(name='Mie Goreng', price=12000, restaurant=self.restaurant)

    def test_toggle_food_fav_success(self):
        data = json.dumps({'selected_items': [self.food1.id, self.food2.id]})
        response = self.client.post(
            reverse('user:toggle_food_fav'), 
            data=data, 
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True, 'message': 'Favorite foods updated!'})

        self.client_profile.refresh_from_db()
        self.assertIn(self.food1, self.client_profile.favorite_foods.all())
        self.assertIn(self.food2, self.client_profile.favorite_foods.all())

    def test_toggle_food_fav_clear_all(self):
        self.client_profile.favorite_foods.add(self.food1, self.food2)

        data = json.dumps({'selected_items': []})
        response = self.client.post(
            reverse('user:toggle_food_fav'), 
            data=data, 
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True, 'message': 'Favorite foods updated!'})

        self.client_profile.refresh_from_db()
        self.assertEqual(self.client_profile.favorite_foods.count(), 0)

    def test_toggle_food_fav_invalid_json(self):
        data = "invalid_json"
        response = self.client.post(
            reverse('user:toggle_food_fav'), 
            data=data, 
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': False, 'message': 'Invalid JSON format'})

    def test_toggle_food_fav_exception(self):
        data = json.dumps({'selected_items': ['invalid_id']})
        response = self.client.post(
            reverse('user:toggle_food_fav'), 
            data=data, 
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json())
        self.assertEqual(response.json()['success'], False)


class ToggleRestoFavViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.force_login(self.user)

        self.client_profile = ClientProfile.objects.create(user=self.user)

        self.resto1 = Restaurant.objects.create(name='Resto A')
        self.resto2 = Restaurant.objects.create(name='Resto B')

    def test_toggle_resto_fav_success(self):
        data = json.dumps({'selected_items': [self.resto1.id, self.resto2.id]})
        response = self.client.post(
            reverse('user:toggle_resto_fav'), 
            data=data, 
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True, 'message': 'Favorite restaurants updated!'})

        self.client_profile.refresh_from_db()
        self.assertIn(self.resto1, self.client_profile.favorite_restaurants.all())
        self.assertIn(self.resto2, self.client_profile.favorite_restaurants.all())

    def test_toggle_resto_fav_clear_all(self):
        self.client_profile.favorite_restaurants.add(self.resto1, self.resto2)

        data = json.dumps({'selected_items': []})
        response = self.client.post(
            reverse('user:toggle_resto_fav'), 
            data=data, 
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True, 'message': 'Favorite restaurants updated!'})

        self.client_profile.refresh_from_db()
        self.assertEqual(self.client_profile.favorite_restaurants.count(), 0)

    def test_toggle_resto_fav_invalid_json(self):
        data = "invalid_json"
        response = self.client.post(
            reverse('user:toggle_resto_fav'), 
            data=data, 
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': False, 'message': 'Invalid JSON format'})

    def test_toggle_resto_fav_exception(self):
        data = json.dumps({'selected_items': ['invalid_id']})
        response = self.client.post(
            reverse('user:toggle_resto_fav'), 
            data=data, 
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json())
        self.assertEqual(response.json()['success'], False)