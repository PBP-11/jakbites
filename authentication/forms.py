from django.forms import ModelForm, EmailField, CharField, Textarea, ImageField, Select
from django.contrib.auth.forms import UserCreationForm
from main.models import *
# from django.utils.html import strip_tags

class ClientRegistrationForm(UserCreationForm):
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(ClientRegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full p-2 bg-gray-200 border-none'

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            Client.objects.create(user=user)
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