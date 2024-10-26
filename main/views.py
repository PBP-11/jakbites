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
    query = request.GET.get('query', '')  # Get the query from the GET request

    # Perform a case-insensitive search using 'icontains' for partial matches
    results = Food.objects.filter(
        Q(name__icontains=query) |  # Search in Food name
        # Q(category__icontains=query) |  # Search in related Restaurant name
        Q(restaurant__name__icontains=query)  # Search in related Restaurant name
    ).select_related('restaurant')  # Optimize the query by using select_related

    # Serialize the results with restaurant details
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

    return JsonResponse(serialized_results, safe=False)  # Return the serialized results as JSON

def search_on_full(request):
    query = request.GET.get('query', '')  # Get the query from the GET request
    filter_value = request.GET.get('filter', 'all')  # Get the filter value
    sort_value = request.GET.get('sort', 'none')  # Get the sort value

    # Start with a basic query using the search term
    results = Food.objects.all()

    # Apply filtering
    if filter_value == 'food':
        results = results.filter(Q(name__icontains=query))
    elif filter_value == 'restaurant':
        results = results.filter(Q(restaurant__name__icontains=query))
    else:
        results = results.filter(
            Q(name__icontains=query) | Q(restaurant__name__icontains=query)
        ).select_related('restaurant')

    # Apply sorting
    if sort_value == 'price_asc':
        results = results.order_by('price')
    elif sort_value == 'price_desc':
        results = results.order_by('-price')
    elif sort_value == 'alpha_asc':
        results = results.order_by('name')
    elif sort_value == 'alpha_desc':
        results = results.order_by('-name')

    # Check if the request is an AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('result_kepotong.html', {'results': results})
        return JsonResponse({'html': html})

    # For normal page loads, render the full page
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
    query = request.GET.get('query', '')  # Get the query from the GET request

    # Start with a basic query using the search term
    results = Restaurant.objects.all()

    # Apply filtering
    results = results.filter(
        Q(name__icontains=query)
    )

    # For normal page loads, render the full page
    context = {
        'results': results,
    }
    return render(request, 'resto.html', context)

#     type = request.GET.get('filter_option', 'all')
    
#     return JsonResponse({'filter_option': filter_option})

# def search_instance(request):
#     query = request.GET.get('query')
#     if query:
#         # Perform a case-insensitive search using 'icontains' for partial matches
#         results = Food.objects.filter(
#             Q(name__icontains=query) |  # Search in Food name
#             Q(category__icontains=query) |  # Search in Food category
#             Q(restaurant__name__icontains=query)  # Search in related Restaurant name
#         )
        
#         if results.exists():
#             # Serialize the results with restaurant names
#             serialized_results = [
#                 {
#                     'name': food.name,
#                     'category': food.category,
#                     'price': food.price,
#                     'restaurant': food.restaurant.name  # Get the restaurant name directly
#                 } for food in results
#             ]
#             request.session['search_results'] = serialized_results  # Store the serialized results
#             return redirect('main:search_results')
        
#         else:
#             return render(request, 'att.html', {
#                 'query': query,
#                 'error_message': f'No results found for "{query}". Please try a different search term.'
#             })

#     return redirect('main:show_att')

# def search_results(request):
#     results = request.session.get('search_results', [])

#     # Clear the results from session after using them
#     if 'search_results' in request.session:
#         del request.session['search_results']
        
#     if results == []:
#         return redirect('main:show_att')
    
#     return render(request, 'results.html', {
#         'results': results  # Pass results to the template
#     })

# def user_login(request):
#     form = AuthenticationForm()
    
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             response = HttpResponseRedirect(reverse("main:show_att"))
#             response.set_cookie('last_login', str(datetime.datetime.now()))
#             return response
#         else:
#             messages.error(request, "Invalid username or password. Please try again.") 

#     context = {'form': form}
#     return render(request, 'login.html', context)


# def search_instance(request):
#     return render(request, "search_instance.html", )