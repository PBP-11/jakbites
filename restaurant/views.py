from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Restaurant, Food, ReviewRestaurant
from django.http import HttpResponse, JsonResponse
import logging

logger = logging.getLogger(__name__)

# Helper function to calculate average rating for a restaurant
def calculate_avg_rating(restaurant):
    reviews = ReviewRestaurant.objects.filter(restaurant=restaurant)
    if reviews.exists():
        total_rating = sum(review.rating for review in reviews)
        avg_rating = total_rating / reviews.count()
        return round(avg_rating, 1)
    return 0.0

@login_required
def restaurant_detail(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    food = Food.objects.filter(restaurant=restaurant)
    reviews = ReviewRestaurant.objects.filter(restaurant=restaurant)
    avg_rating = calculate_avg_rating(restaurant)

    context = {
        'restaurant': restaurant,
        'food': food,
        'review': reviews,
        'avg_rating': avg_rating,
    }

    return render(request, 'restaurant/restaurant_detail.html', context)

@login_required
def push_review(request):
    if request.method == "POST":
        restaurant_id = request.POST.get('restaurant_id')
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)

        review = ReviewRestaurant()
        review.restaurant = restaurant
        review.user = request.user
        review.rating = int(request.POST.get('rating', 0))
        review.review = request.POST.get('review', '')
        review.save()

        avg_rating = calculate_avg_rating(restaurant)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': 'Review successfully submitted!',
                'review': {
                    'user': request.user.username,
                    'rating': review.rating,
                    'review': review.review,
                },
                'avg_rating': avg_rating,
            }, status=200)
        else:
            return redirect('restaurant:restaurant', id=restaurant_id)
    
    return HttpResponse("⛔ Forbidden: Invalid request method.", status=405)

@login_required
def delete_review(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        review = ReviewRestaurant.objects.filter(restaurant=restaurant, user=request.user).first()

        if review:
            review.delete()
            avg_rating = calculate_avg_rating(restaurant)

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'avg_rating': avg_rating,
                    'message': 'Review successfully deleted!',
                }, status=200)
            else:
                return redirect('restaurant:restaurant', id=restaurant_id)
        else:
            return HttpResponse("⛔ Forbidden: You do not have permission to delete this review.", status=403)

    return HttpResponse("⛔ Forbidden: Invalid request method.", status=405)

def fetch_reviews(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    reviews = ReviewRestaurant.objects.filter(restaurant=restaurant).values('user__username', 'rating', 'review')
    reviews_list = list(reviews)  # Convert queryset to list

    return JsonResponse({
        'status': 'success',
        'reviews': reviews_list
    })