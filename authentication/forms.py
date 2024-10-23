from django.forms import ModelForm
from main.models import *
# from django.utils.html import strip_tags

class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'location']

class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'description', 'category', 'restaurant', 'price']