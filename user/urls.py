from django.urls import path
from user.views import profile_view, upload_profile_picture, change_name, change_description, change_password


urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('profile/upload-profile-picture/', upload_profile_picture, name='upload_profile_picture'),  # Tambahkan ini
    path('profile/change-name/', change_name, name='change_name'),
    path('profile/change-description/', change_description, name='change_description'),
    path('profile/change-password/', change_password, name='change_password'),
]
