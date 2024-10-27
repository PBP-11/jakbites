from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Restaurant, Food, ReviewRestaurant
from django.http import HttpResponse, JsonResponse
import os
from django.urls import reverse

@login_required
def restaurant_detail(request, id):
    # Ambil restoran berdasarkan ID atau tampilkan 404 jika tidak ditemukan
    restaurant = get_object_or_404(Restaurant, id=id)
    food = Food.objects.filter(restaurant=restaurant)
    review = ReviewRestaurant.objects.filter(restaurant=restaurant)
    
    context = {'restaurant': restaurant,
               'food':food,
               'review': review,}
    
    # Kirimkan objek restoran ke template
    return render(request, 'restaurant/restaurant_detail.html', context)

@login_required
def push_review(request):
    if request.method == "POST":
        restaurant_id = request.POST['restaurant_id']
        
        # Simpan review
        review = ReviewRestaurant()
        review.restaurant = Restaurant.objects.get(id=restaurant_id)
        review.user = request.user
        review.rating = request.POST['rating']
        review.review = request.POST.get('review', '')
        review.save()
        
        # Cek jika request berasal dari Ajax
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': 'Review successfully submitted!',
                'review': {
                    'user': request.user.username,
                    'rating': review.rating,
                    'review': review.review,
                }
            }, status=200)
        else:
            return redirect('restaurant:restaurant', id=restaurant_id)
    
    return HttpResponse("⛔ Forbidden: Invalid request method.", status=405)

@login_required  # Ensure that only logged-in users can delete reviews
def delete_review(request, restaurant_id):
    # Get the restaurant object by ID
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    # Ensure the request is a POST (since it's triggered by the form)
    if request.method == 'POST':
        # Find the review by the logged-in user for the current restaurant
        review = ReviewRestaurant.objects.filter(restaurant=restaurant, user=request.user).first()

        # If the review exists, delete it
        if review:
            review.delete()
            # Optionally, redirect back to the same restaurant page after deletion
            return redirect('restaurant:restaurant', id=restaurant_id)
        else:
            # If the user does not have a review, return a forbidden response
            return HttpResponse("⛔ Forbidden: You do not have permission to delete this review.", status=403)

    # If it's not a POST request, return forbidden (this should not happen in normal cases)
    return HttpResponse("⛔ Forbidden: Invalid request method.", status=405)
