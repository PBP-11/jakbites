from django.db import models

# class MoodEntry(models.Model):
#     mood = models.CharField(max_length=255)
#     time = models.DateField(auto_now_add=True)
#     feelings = models.TextField()
#     mood_intensity = models.IntegerField()

from django.contrib.auth.models import User

# semua class secara default sudah memiliki attribute 'id' sebagai primary key

class Restaurant(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=150)

class Food(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    category = models.CharField(max_length=150)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    price = models.IntegerField()

class ReviewRestaurant(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()  # 1-5 review scale
    review = models.TextField()

class ReviewFood(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()  # 1-5 review scale
    review = models.TextField()

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # inherit attribut: username, email, password

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # inherit attribut: username, email, password
    favorite_restaurants = models.ManyToManyField(Restaurant) # dapat juga di akses di Restaurant
    favorite_foods = models.ManyToManyField(Food) # dapat juga di akses di Food

