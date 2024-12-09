from django.urls import path
from . import views

app_name = 'food'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('add_food_review_flutter/<int:food_id>/', views.add_food_review_flutter, name='add_food_review_flutter'),
    path('delete_food_review_flutter/<int:review_id>/', views.delete_food_review_flutter, name='delete_food_review_flutter'),
    path('get_food_review/', views.get_food_review, name='get_food_review'),
]