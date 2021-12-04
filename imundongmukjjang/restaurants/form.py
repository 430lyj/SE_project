from django import forms
from .models import Restaurant, Menu_Price


class RestaurantInput(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'phone', 'category']

class MenuInput(forms.ModelForm):
    class Meta:
        model = Menu_Price
        fields = ['menu', 'price', 'restaurant']