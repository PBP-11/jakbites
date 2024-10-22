from django.urls import path
from main.views import show_att

app_name = 'main'

urlpatterns = [
    path('', show_att, name='show_att'),
    # path('login/', user_login, name = "user_login")
    # path('search/', search_instance, name = 'search_instance')
]