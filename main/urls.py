from django.urls import path
from main.views import *

app_name = 'main'

urlpatterns = [
    path('', show_att, name='show_att'),
    path('search/', search_instance, name = 'search_instance'),
    path('search_page/', search_on_full, name = 'search_on_full'),
    path('search_resto/', search_on_resto, name = 'search_on_resto'),
    path('about_us/', about_us, name = 'about_us'),
    path('logout/', logout_user, name = 'logout'),
    path('json_restaurant/', show_json_restaurant, name = 'json_restaurant'),
    path('json_review_restaurant/', show_json_review_restaurant, name = 'json_review_restaurant'),
    # path('login/', user_login, name = "user_login")
]
