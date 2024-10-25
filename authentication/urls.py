from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('admin/', show_admin_page, name='show_admin_page'),
    path('admin/add_restaurant/', add_restaurant, name='add_restaurant'),
    path('admin/add_food/', add_food, name='add_food'),
    path('admin/search/', search, name='search'),
    path('admin/delete_restaurant/', delete_restaurant, name='delete_restaurant'),
    path('admin/delete_food/', delete_food, name='delete_food'),
    path('admin/get_restaurant/', get_restaurant, name='get_restaurant'),
    path('admin/get_food/', get_food, name='get_food'),
]