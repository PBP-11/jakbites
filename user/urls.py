from django.urls import path
from user.views import *


urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('profile/upload-profile-picture/', upload_profile_picture, name='upload_profile_picture'),
    path('profile/change-name/', change_name, name='change_name'),
    path('profile/change-description/', change_description, name='change_description'),
    path('profile/change-password/', change_password, name='change_password'),
    path('toggle_resto_fav/', toggle_resto_fav, name='toggle_resto_fav'),
    path('toggle_food_fav/', toggle_food_fav, name='toggle_food_fav'),
]

