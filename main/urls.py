from django.urls import path
from main.views import show_att, search_instance

app_name = 'main'

urlpatterns = [
    path('', show_att, name='show_att'),
    path('search/', search_instance, name = 'search_instance'),
    # path('search_results/', search_results, name = 'search_results'),
    # path('login/', user_login, name = "user_login")
    
]