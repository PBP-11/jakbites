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
from django.views.decorators.http import require_POST, require_GET

def register(request):
    if request.method == "POST":
        form = ClientRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('authentication:user_login')
    else:
        form = ClientRegistrationForm()
    context = {'form': form}
    return render(request, 'register.html', context)

def user_login(request):
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
    if not Admin.objects.filter(user=request.user).exists():
        messages.error(request, "You do not have permission to view this page.")
        return redirect('authentication:user_login')
    
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
@require_POST
def add_food(request):
    data = json.loads(request.body)
    name = data.get('name')
    description = data.get('description')
    category = data.get('category')
    restaurant_id = data.get('restaurant_id')
    price = data.get('price')

    if not all([name, description, category, restaurant_id, price]):
        return JsonResponse({'success': False, 'error': 'All fields are required.'}, status=400)

    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except Restaurant.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Selected restaurant does not exist.'}, status=404)

    food = Food.objects.create(
        name=name,
        description=description,
        category=category,
        restaurant=restaurant,
        price=price
    )

    return JsonResponse({
        'success': True,
        'food': {
            'id': food.id,
            'name': food.name,
            'description': food.description,
            'category': food.category,
            'restaurant': food.restaurant.id,
            'price': food.price
        }
    })

def search(request):
    search_type = request.GET.get('type')
    query = request.GET.get('query')
    if search_type == 'restaurant':
        results = Restaurant.objects.filter(name__icontains(query))
        data = [{'id': r.id, 'name': r.name, 'location': r.location} for r in results]
    else:
        results = Food.objects.filter(name__icontains(query))
        data = [{'id': f.id, 'name': f.name, 'description': f.description, 'category': f.category, 'restaurant': {'name': f.restaurant.name}, 'price': f.price} for f in results]
    return JsonResponse({'results': data})

def get_restaurant(request):
    restaurant_id = request.GET.get('id')
    restaurant = Restaurant.objects.get(id=restaurant_id)
    return JsonResponse({'success': True, 'restaurant': {'name': restaurant.name, 'location': restaurant.location}})

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

@csrf_exempt
@require_POST
def edit_restaurant(request):
    restaurant_id = request.GET.get('id')
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except Restaurant.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Restaurant not found'})

    form = RestaurantForm(request.POST, instance=restaurant)
    if form.is_valid():
        form.save()
        return JsonResponse({
            'success': True,
            'restaurant': {
                'id': restaurant.id,
                'name': restaurant.name,
                'location': restaurant.location
            }
        })
    return JsonResponse({'success': False, 'errors': form.errors})


@csrf_exempt
@login_required(login_url='authentication/login')
@require_POST
def edit_food(request):
    data = json.loads(request.body)
    food_id = data.get('id')
    name = data.get('name')
    description = data.get('description')
    category = data.get('category')
    restaurant_id = data.get('restaurant_id')
    price = data.get('price')

    if not all([food_id, name, description, category, restaurant_id, price]):
        return JsonResponse({'success': False, 'error': 'All fields are required.'}, status=400)

    try:
        food = Food.objects.get(id=food_id)
    except Food.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Food item does not exist.'}, status=404)

    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except Restaurant.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Selected restaurant does not exist.'}, status=404)

    food.name = name
    food.description = description
    food.category = category
    food.restaurant = restaurant
    food.price = price
    food.save()

    return JsonResponse({
        'success': True,
        'food': {
            'id': food.id,
            'name': food.name,
            'description': food.description,
            'category': food.category,
            'restaurant': food.restaurant.id,
            'price': food.price
        }
    })

@csrf_exempt
def login_flutter(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Status login sukses.
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login sukses!",
                "user": user,
                # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)

@csrf_exempt
def register_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        email = data['email']
        password1 = data['password1']
        password2 = data['password2']

        # Check if the passwords match
        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)
        
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username already exists."
            }, status=400)
        
        # Create the new user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        
        return JsonResponse({
            "username": user.username,
            "status": 'success',
            "message": "User created successfully!"
        }, status=200)
    
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)

@csrf_exempt
def logout_flutter(request):
    username = request.user.username

    try:
        logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)

@csrf_exempt
def create_restaurant_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_restaurant = Restaurant.objects.create(
            name=data['name'],
            location=data['location']
        )
        new_restaurant.save()
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
@require_POST
def create_food_flutter(request):
    try:
        data = json.loads(request.body)
        name = data.get('name')
        description = data.get('description')
        category = data.get('category')
        restaurant_id = data.get('restaurant_id')  # Ensure key is 'restaurant_id'
        price = data.get('price')

        if not all([name, description, category, restaurant_id, price]):
            return JsonResponse({'status': False, 'message': 'All fields are required.'}, status=400)

        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return JsonResponse({'status': False, 'message': 'Selected restaurant does not exist.'}, status=404)

        food = Food.objects.create(
            name=name,
            description=description,
            category=category,
            restaurant=restaurant,
            price=price
        )

        return JsonResponse({'status': 'success', 'message': 'Food created successfully.'}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'status': False, 'message': 'Invalid JSON.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)}, status=500)

@csrf_exempt
def get_restaurants_flutter(request):
    restaurants = Restaurant.objects.all()
    data = [{
        'model': 'main.restaurant',
        'pk': r.id,
        'fields': {
            'name': r.name,
            'location': r.location
        }
    } for r in restaurants]
    return JsonResponse(data, safe=False)

@csrf_exempt
def get_foods_flutter(request):
    foods = Food.objects.all()
    data = [{
        'model': 'main.food',
        'pk': f.id,
        'fields': {
            'name': f.name,
            'description': f.description,
            'category': f.category,
            'restaurant': f.restaurant.id,
            'price': f.price
        }
    } for f in foods]
    return JsonResponse(data, safe=False)

@csrf_exempt
def edit_restaurant_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            restaurant = Restaurant.objects.get(id=data['id'])
            restaurant.name = data['name']
            restaurant.location = data['location']
            restaurant.save()
            return JsonResponse({"status": "success"}, status=200)
        except Restaurant.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Restaurant not found"}, status=404)
    else:
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def edit_food_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            food = Food.objects.get(id=data['id'])
            food.name = data['name']
            food.description = data['description']
            food.category = data['category']
            
            # Get restaurant by ID
            try:
                restaurant = Restaurant.objects.get(id=data['restaurant'])
                food.restaurant = restaurant
            except Restaurant.DoesNotExist:
                return JsonResponse({
                    "status": "error",
                    "message": "Restaurant not found."
                }, status=404)
            
            food.price = data['price']
            food.save()
            
            return JsonResponse({
                "status": "success",
                "message": "Food updated successfully.",
                "food": {
                    "id": food.id,
                    "name": food.name,
                    "description": food.description,
                    "category": food.category,
                    "restaurant": food.restaurant.id,
                    "price": food.price
                }
            }, status=200)
        except Food.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "Food not found."
            }, status=404)
        except KeyError as e:
            return JsonResponse({
                "status": "error",
                "message": f"Missing required field: {str(e)}"
            }, status=400)
    else:
        return JsonResponse({
            "status": "error",
            "message": "Invalid request method"
        }, status=400)

@csrf_exempt
def delete_restaurant_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            restaurant = Restaurant.objects.get(id=data['id'])
            restaurant.delete()
            return JsonResponse({"status": "success"}, status=200)
        except Restaurant.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Restaurant not found"}, status=404)
    else:
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
@require_POST
def delete_food_flutter(request):
    try:
        data = json.loads(request.body)
        food_id = data.get('id')

        if not food_id:
            return JsonResponse({'status': False, 'message': 'ID is required.'}, status=400)

        try:
            food = Food.objects.get(id=food_id)
        except Food.DoesNotExist:
            return JsonResponse({'status': False, 'message': 'Food not found.'}, status=404)

        food.delete()
        return JsonResponse({'status': 'success', 'message': 'Food deleted successfully.'}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'status': False, 'message': 'Invalid JSON.'}, status=400)

    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)}, status=500)

@csrf_exempt
@require_GET
def get_restaurants(request):
    restaurants = Restaurant.objects.all()
    data = [
        {
            'id': restaurant.id,
            'name': restaurant.name,
            'location': restaurant.location
        }
        for restaurant in restaurants
    ]
    return JsonResponse({'restaurants': data})

@csrf_exempt
@require_GET
def get_restaurants(request):
    restaurants = Restaurant.objects.all()
    data = [
        {
            'id': restaurant.id,
            'name': restaurant.name,
            'location': restaurant.location
        }
        for restaurant in restaurants
    ]
    return JsonResponse({'restaurants': data})