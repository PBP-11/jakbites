from django.urls import path
from . import views
from restaurant.views import *

app_name = 'restaurant'

urlpatterns = [
    path('<int:id>/', restaurant_detail, name='restaurant'),
    path('push_review/', push_review, name='push_review'),
    path('<int:restaurant_id>/delete_review/', delete_review, name='delete_review'),
]