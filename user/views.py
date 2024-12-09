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

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Client

import base64
from django.core.files.base import ContentFile

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

        return redirect('user:profile')  

    return redirect('user:profile')

@login_required
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
@login_required
@csrf_exempt  
def change_description(request):
    if request.method == "POST":
        new_description = request.POST.get('new_value')
        if not new_description:
            return JsonResponse({'status': 'error', 'message': 'Description is required.'}, status=400)

        try:
            client = request.user.client  
            client.description = new_description
            client.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


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


@login_required
def get_client_data(request):
    try:
        client = Client.objects.get(user=request.user)

        client_data = {
            'username': request.user.username,
            'profile_picture': client.profile_picture.url if client.profile_picture else None,
            'description': client.description,
            'favorite_restaurants': list(client.favorite_restaurants.values('id', 'name', 'location')),
            'favorite_foods': list(client.favorite_foods.values('id', 'name', 'category', 'price')),
        }

        print(client_data)
        print("sukses")
        return JsonResponse({'success': True, 'data': client_data})
        

    except Client.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Client profile not found'}, status=404)

@login_required
@csrf_exempt 
@require_POST
def change_description_flutter(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_description = data.get('new_value', '').strip()

            if not new_description:
                return JsonResponse({'status': 'error', 'message': 'Description is required.'}, status=400)

            client = Client.objects.get(user=request.user)
            client.description = new_description
            client.save()

            updated_data = {
                'username': request.user.username,
                'description': client.description,
            }

            return JsonResponse({
                'status': 'success',
                'message': 'Description updated successfully!',
                'data': updated_data
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'}, status=400)
        except Client.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Client profile not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@login_required
@csrf_exempt
@require_POST
def change_password_flutter(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            current_password = data.get('current_password', '').strip()
            new_password = data.get('new_password', '').strip()

            if not current_password or not new_password:
                return JsonResponse(
                    {'status': 'error', 'message': 'Both current and new passwords are required.'},
                    status=400
                )

            user = request.user  
            if not user.check_password(current_password):
                return JsonResponse(
                    {'status': 'error', 'message': 'Current password is incorrect.'},
                    status=400
                )
            user.set_password(new_password)
            user.save()
            updated_data = {
                'username': user.username,
            }
            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'Password changed successfully!',
                    'data': updated_data
                },
                status=200
            )
        except json.JSONDecodeError:
            return JsonResponse(
                {'status': 'error', 'message': 'Invalid JSON format.'},
                status=400
            )
        except Exception as e:
            return JsonResponse(
                {'status': 'error', 'message': str(e)},
                status=500
            )
    return JsonResponse(
        {'status': 'error', 'message': 'Invalid request method.'},
        status=405
    )


@login_required
@csrf_exempt 
@require_POST
def change_username_flutter(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_username = data.get('new_value', '').strip()

            if not new_username:
                return JsonResponse({'status': 'error', 'message': 'Description is required.'}, status=400)

            user = request.user
            user.username = new_username
            user.save()

            updated_data = {
                'username': user.username,
                'description': user.client.description,
            }

            return JsonResponse({
                'status': 'success',
                'message': 'Description updated successfully!',
                'data': updated_data
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'}, status=400)
        except Client.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Client profile not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


@login_required
@csrf_exempt
@require_POST
def upload_profile_picture_flutter(request):
    try:
        data = json.loads(request.body)
        profile_picture_base64 = data.get('profile_picture', '')
        
        if not profile_picture_base64:
            return JsonResponse({'status': 'error', 'message': 'No profile picture provided.'}, status=400)
        
        format, imgstr = profile_picture_base64.split(';base64,') 
        ext = format.split('/')[-1] 
        img_data = ContentFile(base64.b64decode(imgstr), name=f'profile_pic.{ext}')
        
        client = Client.objects.get(user=request.user)
        client.profile_picture = img_data
        client.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Profile picture updated successfully!',
            'data': {
                'profile_picture': client.profile_picture.url if client.profile_picture else None
            }
        }, status=200)
    except Client.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Client profile not found.'}, status=404)
    except (ValueError, IndexError):
        return JsonResponse({'status': 'error', 'message': 'Invalid image format.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    

@login_required
def get_all_restaurants_flutter(request):
    try:
        restaurants = Restaurant.objects.all().values('id', 'name', 'location')
        restaurants_list = list(restaurants)
        return JsonResponse({'status': 'success', 'data': restaurants_list}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
def get_all_foods_flutter(request):
    try:
        foods = Food.objects.all().values('id', 'name', 'category', 'price')
        foods_list = list(foods)
        return JsonResponse({'status': 'success', 'data': foods_list}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
@csrf_exempt
@require_POST
def update_favorite_restaurants_flutter(request):
    try:
        data = json.loads(request.body)
        selected_ids = data.get('favorite_restaurants', [])
        if not isinstance(selected_ids, list):
            return JsonResponse({'status': 'error', 'message': 'favorite_restaurants must be a list.'}, status=400)
        
        client = Client.objects.get(user=request.user)
        valid_restaurants = Restaurant.objects.filter(id__in=selected_ids)
        
        client.favorite_restaurants.set(valid_restaurants)
        
        print(f"Selected IDs: {valid_restaurants}")

        return JsonResponse({'status': 'success', 'message': 'Favorite restaurants updated successfully!'}, status=200)
    except Client.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Client profile not found.'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
@csrf_exempt
@require_POST
def update_favorite_foods_flutter(request):
    try:
        data = json.loads(request.body)
        selected_ids = data.get('favorite_foods', [])
        if not isinstance(selected_ids, list):
            return JsonResponse({'status': 'error', 'message': 'favorite_foods must be a list.'}, status=400)
        
        client = Client.objects.get(user=request.user)
        valid_foods = Food.objects.filter(id__in=selected_ids)
        client.favorite_foods.set(valid_foods)
        
        return JsonResponse({'status': 'success', 'message': 'Favorite foods updated successfully!'}, status=200)
    except Client.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Client profile not found.'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)