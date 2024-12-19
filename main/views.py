from main.models import *
from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.models import Restaurant, Food, ReviewRestaurant, ReviewFood, Admin, Client
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string

import json


@login_required(login_url='/authentication/login/')
def show_att(request):
    try:
        client = Client.objects.get(user=request.user)
        context = {
            'profpic': client.profile_picture,
            'name': client.user.username,
        }
    except Client.DoesNotExist:
        context = {
            'profpic': None,
            'name': request.user.username,
        }
        
    return render(request, "att.html", context)


def search_instance(request):
    query = request.GET.get('query', '')  

    results = Food.objects.filter(
        Q(name__icontains=query) |  
        Q(restaurant__name__icontains=query) 
    ).select_related('restaurant')  

    serialized_results = [
        {   
            'food_id': food.id,
            'food_name': food.name,
            'category': food.category,
            'price': food.price,
            'description': food.description,
            'restaurant': {
                'restaurant_name': food.restaurant.name,
                'location': food.restaurant.location,
                'restaurant_id': food.restaurant.id,
            }
        } for food in results
    ]

    return JsonResponse(serialized_results, safe=False) 

def search_on_full(request):
    query = request.GET.get('query', '')  
    filter_value = request.GET.get('filter', 'all')
    sort_value = request.GET.get('sort', 'none') 

    results = Food.objects.all()

    if filter_value == 'food':
        results = results.filter(Q(name__icontains=query))
    elif filter_value == 'restaurant':
        results = results.filter(Q(restaurant__name__icontains=query))
    else:
        results = results.filter(
            Q(name__icontains=query) | Q(restaurant__name__icontains=query)
        ).select_related('restaurant')

    if sort_value == 'price_asc':
        results = results.order_by('price')
    elif sort_value == 'price_desc':
        results = results.order_by('-price')
    elif sort_value == 'alpha_asc':
        results = results.order_by('name')
    elif sort_value == 'alpha_desc':
        results = results.order_by('-name')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('result_kepotong.html', {'results': results})
        return JsonResponse({'html': html})

    context = {
        'results': results,
        'filtered': filter_value,
        'sort': sort_value,
        'query': query
    }
    return render(request, 'results.html', context)

def about_us(request):
    return render(request, 'about_us.html')

def search_on_resto(request):
    query = request.GET.get('query', '')  

    results = Restaurant.objects.all()

    results = results.filter(
        Q(name__icontains=query)
    )

    context = {
        'results': results,
    }
    return render(request, 'resto.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('authentication:user_login'))
    response.delete_cookie('last_login')
    return response

def show_json_restaurant(request):
    data = Restaurant.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_review_restaurant(request):
    data = ReviewRestaurant.objects.all().select_related('user')
    # print(data[0].user)

    serealized_data = []
    for i in data:
        i_data = {
            "restaurant" : i.restaurant.id,
            "userID" : i.pk,
            "rating" : i.rating,
            "review" : i.review,
            "userName" : i.user.username,
            'ID' : i.pk,
        }
        serealized_data.append(i_data)

    # return HttpResponse(serializers.serialize("json", data), content_type="application/json")
    return JsonResponse(
        {
            "status" : 200,
            "message" : "success",
            "data": serealized_data
        }
    )

def show_json_food(request):
    data = Food.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_review_food(request):
    data = ReviewFood.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


from django.http import JsonResponse
from django.db.models import Q
from .models import Restaurant, Food

def search_on_resto_json(request):
    query = request.GET.get('query', '')
    results = Restaurant.objects.filter(name__icontains=query)

    data = []
    for r in results:
        data.append({
            'id': r.id,
            'foodName': r.name,         # Mapping restaurant name to 'foodName' for consistency
            'description': r.location,  # Using location as description
            'category': 'resto'         # Setting category to 'resto' since these are restaurants
        })

    return JsonResponse(data, safe=False)

def search_on_food_json(request):
    query = request.GET.get('query', '')
    results = Food.objects.filter(name__icontains=query)

    data = []
    for f in results:
        data.append({
            'id': f.id,
            'foodName': f.name,
            'description': f.description,
            'category': f.category,
            # If needed, you can add other fields like:
            # 'price': f.price,
            # 'restaurant': f.restaurant.name,
        })

    return JsonResponse(data, safe=False)

