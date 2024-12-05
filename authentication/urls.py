from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='user_login'),
    path('admin/', show_admin_page, name='show_admin_page'),
    path('admin/add_restaurant/', add_restaurant, name='add_restaurant'),
    path('admin/add_food/', add_food, name='add_food'),
    path('admin/search/', search, name='search'),
    path('admin/delete_restaurant/', delete_restaurant, name='delete_restaurant'),
    path('admin/delete_food/', delete_food, name='delete_food'),
    path('admin/get_restaurant/', get_restaurant, name='get_restaurant'),
    path('admin/get_food/', get_food, name='get_food'),
    path('admin/edit_restaurant/', edit_restaurant, name='edit_restaurant'),
    path('admin/edit_food/', edit_food, name='edit_food'),
    path('login_flutter/', login_flutter, name='login_flutter'),
    path('register_flutter/', register_flutter, name='register_flutter'),
    path('logout_flutter/', logout_flutter, name='logout_flutter'),
    path('create_restaurant_flutter/', create_restaurant_flutter, name='create_restaurant_flutter'),
    path('edit_restaurant_flutter/', edit_restaurant_flutter, name='edit_restaurant_flutter'),
    path('delete_restaurant_flutter/', delete_restaurant_flutter, name='delete_restaurant_flutter'),
    path('get_restaurants_flutter/', get_restaurants_flutter, name='get_restaurants_flutter'),
    path('create_food_flutter/', create_food_flutter, name='create_food_flutter'),
    path('get_foods_flutter/', get_foods_flutter, name='get_foods_flutter'),
    path('edit_food_flutter/', edit_food_flutter, name='edit_food_flutter'),
    path('delete_food_flutter/', delete_food_flutter, name='delete_food_flutter'),
]