from django.forms import ModelForm, EmailField, CharField, Textarea, ImageField, Select
from django.contrib.auth.forms import UserCreationForm
from main.models import *
# from django.utils.html import strip_tags

class ClientRegistrationForm(UserCreationForm):
    email = EmailField(required=True)
    profile_picture = ImageField(required=False)
    description = CharField(widget=Textarea, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'profile_picture', 'description']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            client = Client(user=user, profile_picture=self.cleaned_data['profile_picture'], description=self.cleaned_data['description'])
            client.save()
        return user

class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'location']

class FoodForm(ModelForm):
    restaurant_name = CharField(max_length=150, required=True, label='Restaurant')

    class Meta:
        model = Food
        fields = ['name', 'description', 'category', 'restaurant_name', 'price']