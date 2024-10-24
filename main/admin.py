
# Register your models here.
from django.contrib import admin
from main.models import *

admin.site.register(Restaurant)
admin.site.register(Food)
# admin.site.register(Client)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'get_favorite_restaurants', 'get_favorite_foods', 'profile_picture')

    # Add methods to display ManyToMany fields as comma-separated values
    def get_favorite_restaurants(self, obj):
        return ", ".join([restaurant.name for restaurant in obj.favorite_restaurants.all()])

    def get_favorite_foods(self, obj):
        return ", ".join([food.name for food in obj.favorite_foods.all()])

    get_favorite_restaurants.short_description = 'Favorite Restaurants'
    get_favorite_foods.short_description = 'Favorite Foods'

# Register the Client model
admin.site.register(Client, ClientAdmin)
