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


# @login_required(login_url='/login')
def show_att(request):
    
    context = {
    }

    return render(request, "att.html", context)


def search_instance(request):
    query = request.GET.get('query', '')  # Get the query from the GET request
    if len(query) < 1:
        return JsonResponse([])  # Return an empty JSON array if the query is empty

    # Perform a case-insensitive search using 'icontains' for partial matches
    results = Food.objects.filter(
        Q(name__icontains=query) |  # Search in Food name
        Q(category__icontains=query) |  # Search in related Restaurant name
        Q(restaurant__name__icontains=query)  # Search in related Restaurant name
    ).select_related('restaurant')  # Optimize the query by using select_related

    # Serialize the results with restaurant details
    serialized_results = [
        {
            'food_name': food.name,
            'category': food.category,
            'price': food.price,
            'description': food.description,
            'restaurant': {
                'restaurant_name': food.restaurant.name,
                'location': food.restaurant.location,
            }
        } for food in results
    ]

    return JsonResponse(serialized_results, safe=False)  # Return the serialized results as JSON

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

