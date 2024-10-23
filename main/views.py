from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import *
from django.contrib import messages


# Remove login_required for now
def profile_view(request):
    # Dummy user object for testing purposes
    user = request.user if request.user.is_authenticated else None

    # Render the profile page without requiring login
    return render(request, 'profile.html', {'user': user})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})

def upload_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        try:
            client = Client.objects.get(user=request.user)
            client.profile_picture = request.FILES['profile_picture']
            client.save()

            messages.success(request, 'Foto profil berhasil diperbarui.')
        except Client.DoesNotExist:
            messages.error(request, 'User tidak memiliki profil yang terhubung.')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')

        return redirect('profile')

    return render(request, 'profile.html')