import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from authentication.forms import *
# from main.models import MoodEntry
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.http import JsonResponse

def register(request):
    if request.method == "POST":
        form = ClientRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your account has been successfully created!')
            login(request, user)
            return redirect('main:show_att')
    else:
        form = ClientRegistrationForm()
    context = {'form': form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Check if the user is an admin or client
            if Admin.objects.filter(user=user).exists():
                return HttpResponseRedirect(reverse("authentication:show_admin_page"))
            elif Client.objects.filter(user=user).exists():
                return HttpResponseRedirect(reverse("main:show_att"))
            else:
                return HttpResponseRedirect(reverse("main:show_att"))
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

@login_required(login_url='authentication/login')
def show_admin_page(request):
    restaurant_form = RestaurantForm()
    food_form = FoodForm()
    
    restaurants = Restaurant.objects.all()
    foods = Food.objects.all()
    
    context = {
        'restaurant_form': restaurant_form,
        'food_form': food_form,
        'restaurants': restaurants,
        'foods': foods,
    }
    return render(request, 'admin.html', context)

@csrf_exempt
@login_required(login_url='authentication/login')
def add_restaurant(request):
    if request.method == 'POST':
        restaurant_form = RestaurantForm(request.POST)
        if restaurant_form.is_valid():
            restaurant = restaurant_form.save()
            return JsonResponse({'success': True, 'restaurant': {'name': restaurant.name, 'location': restaurant.location}})
        else:
            return JsonResponse({'success': False, 'errors': restaurant_form.errors})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
@login_required(login_url='authentication/login')
def add_food(request):
    if request.method == 'POST':
        food_form = FoodForm(request.POST)
        if food_form.is_valid():
            restaurant_name = food_form.cleaned_data['restaurant_name']
            try:
                restaurant = Restaurant.objects.get(name=restaurant_name)
            except Restaurant.DoesNotExist:
                return JsonResponse({'success': False, 'errors': {'restaurant_name': ['Restaurant not found']}})
            
            food = food_form.save(commit=False)
            food.restaurant = restaurant
            food.save()
            return JsonResponse({
                'success': True,
                'food': {
                    'name': food.name,
                    'description': food.description,
                    'category': food.category,
                    'restaurant': {
                        'name': food.restaurant.name
                    },
                    'price': food.price
                }
            })
        else:
            return JsonResponse({'success': False, 'errors': food_form.errors})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required(login_url='authentication/login')
def search(request):
    search_type = request.GET.get('type')
    query = request.GET.get('query')
    
    if search_type == 'restaurant':
        results = Restaurant.objects.filter(name__icontains=query)
        data = [{'name': restaurant.name, 'location': restaurant.location} for restaurant in results]
    elif search_type == 'food':
        results = Food.objects.filter(name__icontains=query)
        data = [{'name': food.name, 'description': food.description, 'category': food.category, 'price': food.price, 'restaurant': {'name': food.restaurant.name}} for food in results]
    else:
        return JsonResponse({'success': False, 'error': 'Invalid search type'})
    
    return JsonResponse({'success': True, 'results': data})

@csrf_exempt
@login_required(login_url='authentication/login')
def delete_restaurant(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            restaurant_id = data.get('id')
            restaurant = Restaurant.objects.get(id=restaurant_id)
            restaurant.delete()
            return JsonResponse({'success': True})
        except Restaurant.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Restaurant not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
@login_required(login_url='authentication/login')
def delete_food(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            food_id = data.get('id')
            food = Food.objects.get(id=food_id)
            food.delete()
            return JsonResponse({'success': True})
        except Food.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Food not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# def create_restaurant(request):
#     form = RestaurantForm(request.POST or None)

#     if form.is_valid() and request.method == "POST":
#         mood_entry = form.save(commit=False)
#         mood_entry.user = request.user
#         mood_entry.save()
#         return redirect("authentication:show_admin_page")

#     context = {'form': form}
#     return render(request, "create_mood_entry.html", context)