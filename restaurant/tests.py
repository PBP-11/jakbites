from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Restaurant, ReviewRestaurant

User = get_user_model()

class RestaurantReviewTests(TestCase):

    def setUp(self):
        # Buat user untuk pengujian
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Buat restoran untuk pengujian
        self.restaurant = Restaurant.objects.create(name='Test Restaurant', location='Jakarta.')
        
        # Simulasikan login user
        self.client.login(username='testuser', password='testpass')

    def test_push_review(self):
        # URL untuk menambahkan ulasan
        url = reverse('restaurant:push_review')
        
        # Data untuk pengiriman ulasan
        data = {
            'restaurant_id': self.restaurant.id,
            'rating': 5,
            'review': 'Amazing food!'
        }
        
        # Kirimkan request POST untuk menambahkan ulasan
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        # Periksa apakah ulasan ditambahkan dengan benar
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'status': 'success',
            'message': 'Review successfully submitted!',
            'review': {
                'user': self.user.username,
                'rating': '5',
                'review': 'Amazing food!'
            }
        })
        self.assertEqual(ReviewRestaurant.objects.count(), 1)  # Pastikan satu ulasan ditambahkan

    def test_delete_review(self):
        # Buat ulasan untuk pengujian penghapusan
        review = ReviewRestaurant.objects.create(
            restaurant=self.restaurant,
            user=self.user,
            rating=5,
            review='Amazing food!'
        )
        
        # URL untuk menghapus ulasan
        url = reverse('restaurant:delete_review', args=[self.restaurant.id])
        
        # Kirimkan request POST untuk menghapus ulasan
        response = self.client.post(url)
        
        # Periksa apakah ulasan dihapus dengan benar
        self.assertEqual(response.status_code, 302)  # Redirect setelah penghapusan
        self.assertEqual(ReviewRestaurant.objects.count(), 0)  # Pastikan ulasan telah dihapus

    def test_push_review_unauthenticated(self):
        # Logout user
        self.client.logout()
        
        # Coba kirimkan ulasan tanpa login
        url = reverse('restaurant:push_review')
        data = {
            'restaurant_id': self.restaurant.id,
            'rating': 5,
            'review': 'Amazing food!'
        }
        response = self.client.post(url, data)
        
        # Periksa status forbidden
        self.assertEqual(response.status_code, 302)  # Seharusnya redirect ke login

    def test_delete_review_unauthorized(self):
        # Buat user lain untuk pengujian
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        
        # Simulasikan login user lain
        self.client.login(username='otheruser', password='otherpass')
        
        # Coba hapus ulasan yang bukan milik user ini
        url = reverse('restaurant:delete_review', args=[self.restaurant.id])
        response = self.client.post(url)
        
        # Periksa status forbidden
        self.assertEqual(response.status_code, 403)  # Harusnya forbidden karena tidak memiliki ulasan

