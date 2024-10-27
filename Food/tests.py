import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Food, ReviewFood, Restaurant

class FoodViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            location='Test Location'
        )
        self.food = Food.objects.create(
            name='Test Food',
            description='Test Description',
            category='Test Category',
            restaurant=self.restaurant,
            price=100
        )
        self.review = ReviewFood.objects.create(
            food=self.food,
            user=self.user,
            rating=5,
            review='Great food!'
        )

    def test_product_list(self):
        response = self.client.get(reverse('food:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_list.html')
        self.assertContains(response, self.food.name)

    def test_product_detail_get(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('food:product_detail', args=[self.food.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_detail.html')
        self.assertContains(response, self.food.name)
        self.assertContains(response, self.review.review)

    def test_product_detail_post(self):
        self.client.login(username='testuser', password='12345')
        data = {
            'rating': 4,
            'review': 'Good food!'
        }
        response = self.client.post(
            reverse('food:product_detail', args=[self.food.id]),
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['avg_rating'], 4.5)

    def test_delete_review(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('food:delete_review', args=[self.review.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(ReviewFood.objects.count(), 0)
