from django.test import TestCase, Client
from django.urls import reverse
from main.models import Food, Restaurant
from django.http import JsonResponse

class MainAppTests(TestCase):
    
    def setUp(self):
        # Create a client to simulate requests
        self.client = Client()

        # Set up any initial data required for testing
        self.restaurant = Restaurant.objects.create(name="Test Restaurant", location="Test Location")
        self.food = Food.objects.create(name="Test Food", category="Test Category", price=10, description="Test Description", restaurant=self.restaurant)

    def test_show_att_view(self):
        # Test the 'show_att' view loads correctly
        response = self.client.get(reverse('main:show_att'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'att.html')

    def test_about_us_view(self):
        # Test the 'about_us' view loads correctly
        response = self.client.get(reverse('main:about_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about_us.html')

    def test_search_instance_view(self):
        # Test the 'search_instance' view with a query
        response = self.client.get(reverse('main:search_instance'), {'query': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response, JsonResponse))
        
        # Check that the JSON response contains the expected data
        data = response.json()
        self.assertTrue(any(food['food_name'] == "Test Food" for food in data))

    def test_search_on_full_view(self):
        # Test the 'search_on_full' view with query, filter, and sort parameters
        response = self.client.get(reverse('main:search_on_full'), {
            'query': 'Test', 
            'filter': 'food', 
            'sort': 'price_asc'
        })
        self.assertEqual(response.status_code, 200)
        
        # Check if the request is AJAX (using X-Requested-With header)
        ajax_response = self.client.get(reverse('main:search_on_full'), {
            'query': 'Test', 
            'filter': 'food', 
            'sort': 'price_asc'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        # Ensure that AJAX response returns JSON data
        self.assertEqual(ajax_response.status_code, 200)
        self.assertTrue(isinstance(ajax_response, JsonResponse))
        
        # Check the structure of the response
        ajax_data = ajax_response.json()
        self.assertIn('html', ajax_data)

    def tearDown(self):
        # Clean up any test data
        self.restaurant.delete()
        self.food.delete()