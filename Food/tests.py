from django.test import TestCase, Client
from django.urls import reverse
from Food.models import Food, ReviewFood, Restaurant  
from django.contrib.auth.models import User

class ViewsTestCase(TestCase):
    def setUp(self):
        # Membuat contoh data untuk restaurant
        self.restaurant = Restaurant.objects.create(name='Restoran 1')

        # Membuat contoh produk dengan restaurant yang valid
        self.product1 = Food.objects.create(
            name='Produk 1',
            price=10000,
            description='Deskripsi Produk 1',
            restaurant=self.restaurant  # Menambahkan restaurant
        )
        self.user = User.objects.create(username='test_user')
        self.client = Client()

    def test_product_list_view(self):
        # Menguji tampilan daftar produk
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_list.html')
        self.assertContains(response, 'Produk 1')

    def test_product_detail_view_get(self):
        # Menguji tampilan detail produk tanpa login
        response = self.client.get(reverse('product_detail', args=[self.product1.id]))
        self.assertEqual(response.status_code, 302)  # Harus redirect ke halaman login
        self.assertRedirects(response, f"/accounts/login/?next=/product/{self.product1.id}/")  # Sesuaikan dengan URL login Anda

        # Login pengguna
        self.client.force_login(self.user)

        # Uji kembali tampilan detail produk setelah login
        response = self.client.get(reverse('product_detail', args=[self.product1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_detail.html')
        self.assertContains(response, self.product1.name)

    def test_product_detail_view_post(self):
        # Menguji penambahan review via POST AJAX
        data = {
            'rating': 5,
            'review': 'Review untuk Produk 1'
        }
        self.client.force_login(self.user)  # Login user untuk menambahkan review
        response = self.client.post(
            reverse('product_detail', args=[self.product1.id]),
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['avg_rating'], 5)
        self.assertEqual(response.json()['username'], 'test_user')
        self.assertEqual(response.json()['rating'], 5)
        self.assertEqual(response.json()['review'], 'Review untuk Produk 1')

    def test_delete_review(self):
        # Menambahkan review untuk dihapus
        review1 = ReviewFood.objects.create(
            food=self.product1,
            user=self.user,
            rating=4,
            review='Review untuk dihapus'
        )

        # Menghapus review via AJAX
        self.client.force_login(self.user)  # Login user yang memiliki review
        response = self.client.post(
            reverse('delete_review', args=[review1.id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['avg_rating'], 0.0)  # Rata-rata rating setelah review 1 dihapus

    def test_delete_review_not_owner(self):
        # Membuat pengguna baru dan review
        other_user = User.objects.create(username='other_user')
        review = ReviewFood.objects.create(
            food=self.product1,
            user=other_user,
            rating=4,
            review='Review dari pengguna lain'
        )

        # Menguji penghapusan review oleh pengguna yang bukan pemilik
        self.client.force_login(self.user)  # Login sebagai pengguna yang bukan pemilik
        response = self.client.post(
            reverse('delete_review', args=[review.id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 403)  # Harusnya 403 Forbidden
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['error'], 'You are not authorized to delete this review.')

    def test_delete_non_existing_review(self):
        # Menguji penghapusan review yang tidak ada
        self.client.force_login(self.user)  # Login sebagai pengguna yang terautentikasi
        response = self.client.post(
            reverse('delete_review', args=[999]),  # ID yang tidak ada
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['error'], 'Review not found.')