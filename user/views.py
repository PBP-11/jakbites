# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from main.models import *
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.views.decorators.http import require_POST
import json
from django.contrib.auth.decorators import login_required






def profile_view(request):
    # try:
    #     user = User.objects.get(username='test1')
    #     login(request, user) 
    # except User.DoesNotExist:
    #     user = None

    user = request.user

    client = Client.objects.filter(user=user).first()

    all_foods = Food.objects.all()
    all_restaurants = Restaurant.objects.all()

    favorite_foods = client.favorite_foods.all() if client else []
    favorite_restaurants = client.favorite_restaurants.all() if client else []

    all_restaurants_json = serializers.serialize('json', all_restaurants)
    all_foods_json = serializers.serialize('json', all_foods)
    favorite_restaurants_json = serializers.serialize('json', favorite_restaurants)
    favorite_foods_json = serializers.serialize('json', favorite_foods)

    context = {
        'user': user,
        'client': client,
        'favorite_restaurants': favorite_restaurants,
        'favorite_foods': favorite_foods,
        'all_foods': all_foods,
        'all_restaurants': all_restaurants,
        'all_restaurants_json': all_restaurants_json,
        'all_foods_json': all_foods_json,
        'favorite_restaurants_json': favorite_restaurants_json,
        'favorite_foods_json': favorite_foods_json,
    }
    return render(request, 'profile.html', context)


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

        return redirect('profile')  

    return redirect('profile')

def change_name(request):
    if request.method == 'POST':
        new_name = request.POST.get('new_value')  
        if new_name:
            user = request.user
            user.username = new_name
            user.save()
            return JsonResponse({'message': 'Username updated successfully!'})
        else:
            return JsonResponse({'error': 'Username cannot be empty.'}, status=400)

@csrf_exempt  
def change_description(request):
    if request.method == 'POST':
        new_description = request.POST.get('new_value') 

        client, created = Client.objects.get_or_create(user=request.user)

        if new_description:
            client.description = new_description
            client.save()
            return JsonResponse({'message': 'Description updated successfully!'})
        else:
            return JsonResponse({'error': 'Description cannot be empty.'}, status=400)

@csrf_exempt  
@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')

        if not request.user.check_password(current_password):
            return JsonResponse({'success': False, 'message': 'Current password is incorrect.'})

        request.user.set_password(new_password)
        request.user.save()

        update_session_auth_hash(request, request.user)

        return JsonResponse({'success': True, 'message': 'Password changed successfully!'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
        
@csrf_exempt  
@require_POST
def toggle_resto_fav(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected_ids = data.get('selected_items', [])

            client = request.user.client
            client.favorite_restaurants.clear()
            if selected_ids:
                favorite_restaurants = Restaurant.objects.filter(id__in=selected_ids)
                client.favorite_restaurants.add(*favorite_restaurants)

            return JsonResponse({'success': True, 'message': 'Favorite restaurants updated!'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON format'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request'})


@csrf_exempt  
@require_POST
def toggle_food_fav(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected_ids = data.get('selected_items', [])

            client = request.user.client
            client.favorite_foods.clear()
            if selected_ids:
                favorite_foods = Food.objects.filter(id__in=selected_ids)
                client.favorite_foods.add(*favorite_foods)

            return JsonResponse({'success': True, 'message': 'Favorite foods updated!'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON format'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request'})


