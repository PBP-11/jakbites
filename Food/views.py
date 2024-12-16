import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Food, ReviewFood
from .forms import ReviewForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

def product_list(request):
    products = Food.objects.all()
    return render(request, 'product_list.html', {'products': products})

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Food, id=product_id)
    reviews = ReviewFood.objects.filter(food=product)

    total_reviews = reviews.count()
    avg_rating = sum([review.rating for review in reviews]) / total_reviews if total_reviews > 0 else 0

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        logger.debug("Received POST data: %s", request.POST)
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.food = product
            review.user = request.user  

            # # Tambahkan user placeholder untuk testing
            # user_placeholder, created = User.objects.get_or_create(username='test_user')
            # review.user = user_placeholder

            # Pastikan teks review disimpan
            review_text = review_form.cleaned_data.get('review')
            if review_text:
                review.review = review_text

            review.save()

            # Perbarui rating dan review setelah submit
            reviews = ReviewFood.objects.filter(food=product)
            total_reviews = reviews.count()
            avg_rating = sum([review.rating for review in reviews]) / total_reviews

            response = {
                'avg_rating': avg_rating,
                'username': review.user.username,
                'rating': review.rating,
                'review': review.review,  
                'id': review.id,
            }
            return JsonResponse(response)
        else:
            logger.error("Form errors: %s", review_form.errors)
            return JsonResponse({'error': 'Invalid form data', 'details': review_form.errors}, status=400)

    review_form = ReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_form': review_form,
    }
    return render(request, 'product_detail.html', context)

def calculate_avg_rating(product):
    reviews = ReviewFood.objects.filter(food=product)
    if reviews.exists():
        total_rating = sum(review.rating for review in reviews)
        avg_rating = total_rating / reviews.count()
        return round(avg_rating, 1)
    return 0.0

@login_required
def delete_review(request, review_id):
    if request.method == 'POST':
        try:
            review = ReviewFood.objects.get(id=review_id)
            
            # Periksa apakah pengguna yang sedang login adalah pemilik review
            if request.user != review.user:
                return JsonResponse({'success': False, 'error': 'You are not authorized to delete this review.'}, status=403)

            product = review.food
            review.delete()

            # Menghitung rata-rata rating setelah review dihapus
            avg_rating = calculate_avg_rating(product)

            return JsonResponse({'success': True, 'avg_rating': avg_rating})
        except ReviewFood.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Review not found.'}, status=404)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

@csrf_exempt  # Only for development. Remove in production.
@login_required  # Ensures that only authenticated users can post reviews.
def add_food_review_flutter(request, food_id):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            rating = data.get('rating')
            review_text = data.get('review')

            # Validate the received data
            if rating is None or review_text is None:
                return JsonResponse(
                    {"status": "error", "message": "Rating and review are required."},
                    status=400
                )
            if not isinstance(rating, int) or not (1 <= rating <= 5):
                return JsonResponse(
                    {"status": "error", "message": "Rating must be an integer between 1 and 5."},
                    status=400
                )
            if not isinstance(review_text, str) or not review_text.strip():
                return JsonResponse(
                    {"status": "error", "message": "Review text cannot be empty."},
                    status=400
                )

            # Retrieve the Food object
            food = get_object_or_404(Food, pk=food_id)

            # Create and save the new review
            new_review = ReviewFood.objects.create(
                food=food,
                user=request.user,  # Correct field name
                rating=rating,
                review=review_text.strip(),
            )
            new_review.save()

            return JsonResponse({"status": "success"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON data."},
                status=400
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)},
                status=500
            )
    else:
        return JsonResponse(
            {"status": "error", "message": "Only POST method is allowed."},
            status=405
        )

@csrf_exempt
def delete_food_review_flutter(request, review_id):
    if request.method == 'POST':
        try:
            # Retrieve the article by ID
            review = ReviewFood.objects.get(id=review_id)
            # Perform the delete operation
            review.delete()
            # Return success response
            return JsonResponse({'success': True, 'message': 'Article deleted successfully'})
        except ReviewFood.DoesNotExist:
            # If the article does not exist
            return JsonResponse({'success': False, 'message': 'Article not found'}, status=404)
        except Exception as e:
            # Handle unexpected errors
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        # If the request is not POST
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

def get_food_review(request):
    reviews = ReviewFood.objects.all()
    review_data = []
    for review in reviews:
        is_author = review.user == request.user
        review_data.append({
            'food': review.food.name,
            'reviewid': review.pk,
            'rating': review.rating,
            'review': review.review,
            'is_author': is_author,
            'author': review.user.username,
        })

    return JsonResponse({'review': review_data})