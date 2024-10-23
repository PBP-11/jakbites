from django.shortcuts import render, get_object_or_404, redirect
from main.models import Food, ReviewFood  
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required

def product_list(request):
    # Mengambil semua produk makanan dari database
    products = Food.objects.all()
    return render(request, 'product_list.html', {'products': products})

@login_required
def product_detail(request, product_id):
    # Mendapatkan detail produk makanan berdasarkan ID
    product = get_object_or_404(Food, id=product_id)
    
    # Mengambil semua ulasan yang terkait dengan produk tersebut
    reviews = ReviewFood.objects.filter(food=product)
    review_form = ReviewForm()

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.food = product
            review.user = request.user
            review.save()
            return redirect('product_detail', product_id=product.id)

    context = {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
    }
    return render(request, 'product_detail.html', context)