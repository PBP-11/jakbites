from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Food, ReviewFood
from .forms import ReviewForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
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