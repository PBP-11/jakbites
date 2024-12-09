from django.urls import path
from user.views import *
from . import views

app_name = 'user'

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('profile/upload-profile-picture/', upload_profile_picture, name='upload_profile_picture'),
    path('profile/change-name/', change_name, name='change_name'),
    path('profile/change-description/', change_description, name='change_description'),
    path('profile/change-password/', change_password, name='change_password'),
    path('toggle_resto_fav/', toggle_resto_fav, name='toggle_resto_fav'),
    path('toggle_food_fav/', toggle_food_fav, name='toggle_food_fav'),
    path('get_client_data/', get_client_data, name='get_client_data'),
    
    path('change-description-flutter/', change_description_flutter, name='change_description_flutter'),
    path('change-username-flutter/', change_username_flutter, name='change_username_flutter'),
    path('change-password-flutter/', change_password_flutter, name='change-password-flutter'),
    path('upload-picture-flutter/', upload_profile_picture_flutter, name='upload_profile_picture_flutter'),
    path('get-all-restaurants-flutter/', get_all_restaurants_flutter, name='get_all_restaurants_flutter'),
    path('get-all-foods-flutter/', get_all_foods_flutter, name='get_all_foods_flutter'),
    path('update-fav-restaurants-flutter/', update_favorite_restaurants_flutter, name='update_favorite_restaurants_flutter'),
    path('update-fav-foods-flutter/', update_favorite_foods_flutter, name='update_favorite_foods_flutter'),

]