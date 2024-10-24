from django import forms
from django.contrib.auth.models import User
from main.models import Client


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['favorite_restaurants', 'favorite_foods']


