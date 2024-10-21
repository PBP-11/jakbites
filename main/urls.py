from django.urls import path
from main.views import show_att

app_name = 'main'

urlpatterns = [
    path('', show_att, name='show_att'),
    # path('search/', search_instance, name = 'search_instance')
]