from django.contrib import admin
from .models import Big_Category, Restaurant, Category, Menu_Price

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(Menu_Price)
admin.site.register(Big_Category)
