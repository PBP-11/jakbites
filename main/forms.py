from django import forms
from main.models import ReviewFood

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewFood
        fields = ['rating', 'review']