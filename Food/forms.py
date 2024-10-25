from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import ReviewFood

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewFood
        fields = ['rating', 'review']  
        widgets = {
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'step': 1, 
            }),
        }