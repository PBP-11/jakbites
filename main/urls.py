from django.urls import path
from main.views import show_att, search_instance, search_on_full, about_us

app_name = 'main'

urlpatterns = [
    path('', show_att, name='show_att'),
    path('search/', search_instance, name = 'search_instance'),
    path('search_page/', search_on_full, name = 'search_on_full'),
    path('about_us/', about_us, name = 'about_us')
    # path('login/', user_login, name = "user_login")
    
]