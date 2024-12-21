from django.urls import path
from main.views import *

app_name = 'main'

urlpatterns = [
    path('', show_att, name='show_att'),
    path('search/', search_instance, name = 'search_instance'),
    path('search_page/', search_on_full, name = 'search_on_full'),
    path('search_resto/', search_on_resto, name = 'search_on_resto'),
    path('search_on_food_json/', search_on_food_json, name = 'search_on_food_json'),
    path('search_on_resto_json/', search_on_resto_json, name = 'search_on_food_json'),
    path('about_us/', about_us, name = 'about_us'),
    path('logout/', logout_user, name = 'logout'),
    path('json_restaurant/', show_json_restaurant, name = 'json_restaurant'),
    path('json_review_restaurant/', show_json_review_restaurant, name = 'json_review_restaurant'),
    # path('login/', user_login, name = "user_login")
    path('json_food/', show_json_food, name = 'json_food'),
    path('json_review_food/', show_json_review_food, name = 'json_review_food'),
]
