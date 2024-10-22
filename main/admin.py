# Register your models here.
from django.contrib import admin
from .models import Restaurant, Food

admin.site.register(Restaurant)
admin.site.register(Food)
