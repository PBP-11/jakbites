from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/upload-profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),  # Tambahkan ini
]
