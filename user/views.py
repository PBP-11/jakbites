from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from main.models import *
from django.contrib import messages
from django.http import JsonResponse



# Remove login_required for now
def profile_view(request):
    # Dummy user object for testing purposes
    user = request.user if request.user.is_authenticated else None

    # Render the profile page without requiring login
    return render(request, 'profile.html', {'user': user})

def upload_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        try:
            client = Client.objects.get(user=request.user)
            client.profile_picture = request.FILES['profile_picture']
            client.save()
            messages.success(request, 'Foto profil berhasil diunggah.')
        except Client.DoesNotExist:
            messages.error(request, 'User tidak memiliki profil yang terhubung.')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')

        return redirect('profile')  # Kembali ke halaman profil

    return redirect('profile')

def change_name(request):
    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        if new_name:
            user = request.user
            user.username = new_name
            user.save()
            return JsonResponse({'message': 'Nama berhasil diubah.'})
        else:
            return JsonResponse({'message': 'Nama tidak boleh kosong.'}, status=400)

def change_description(request):
    if request.method == 'POST':
        new_description = request.POST.get('new_description')
        client = Client.objects.get(user=request.user)
        if new_description is not None:
            client.description = new_description
            client.save()
            return JsonResponse({'message': 'Deskripsi berhasil diubah.'})
        else:
            return JsonResponse({'message': 'Deskripsi tidak boleh kosong.'}, status=400)

def change_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        if new_password:
            user = request.user
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Update session untuk menghindari logout
            return JsonResponse({'message': 'Kata sandi berhasil diubah.'})
        else:
            return JsonResponse({'message': 'Kata sandi tidak boleh kosong.'}, status=400)