import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from authentication.forms import *
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

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
            logout(request)  # Ensure any existing session is logged out
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
@require_POST
def add_restaurant(request):
    form = RestaurantForm(request.POST)
    if form.is_valid():
        restaurant = form.save()
        return JsonResponse({'success': True, 'restaurant': {'id': restaurant.id, 'name': restaurant.name, 'location': restaurant.location}})
    return JsonResponse({'success': False, 'errors': form.errors})

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
                    'id': food.id,
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

def search(request):
    search_type = request.GET.get('type')
    query = request.GET.get('query')
    if search_type == 'restaurant':
        results = Restaurant.objects.filter(name__icontains=query)
        data = [{'id': r.id, 'name': r.name, 'location': r.location} for r in results]
    else:
        results = Food.objects.filter(name__icontains=query)
        data = [{'id': f.id, 'name': f.name, 'description': f.description, 'category': f.category, 'restaurant': {'name': f.restaurant.name}, 'price': f.price} for f in results]
    return JsonResponse({'results': data})

def get_restaurant(request):
    restaurant_id = request.GET.get('id')
    restaurant = Restaurant.objects.get(id=restaurant_id)
    return JsonResponse({'success': True, 'restaurant': {'name': restaurant.name, 'location': restaurant.location}})

@login_required(login_url='authentication/login')
def get_food(request):
    food_id = request.GET.get('id')
    try:
        food = Food.objects.get(id=food_id)
        data = {
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
        }
        return JsonResponse(data)
    except Food.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Food not found'})

@csrf_exempt
@require_POST
def edit_restaurant(request):
    restaurant_id = request.GET.get('id')
    restaurant = Restaurant.objects.get(id=restaurant_id)
    form = RestaurantForm(request.POST, instance=restaurant)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': form.errors})

@csrf_exempt
@require_POST
def edit_food(request):
    food_id = request.GET.get('id')
    food = Food.objects.get(id=food_id)
    form = FoodForm(request.POST, instance=food)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': form.errors})

@csrf_exempt
@require_POST
def delete_restaurant(request):
    data = json.loads(request.body)
    restaurant_id = data.get('id')
    Restaurant.objects.get(id=restaurant_id).delete()
    return JsonResponse({'success': True})

@csrf_exempt
@require_POST
def delete_food(request):
    data = json.loads(request.body)
    food_id = data.get('id')
    Food.objects.get(id=food_id).delete()
    return JsonResponse({'success': True})