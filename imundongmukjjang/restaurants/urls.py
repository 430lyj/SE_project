from django.urls import path
from .views import *

app_name="restaurants"

urlpatterns = [
    path('search/', map_search, name="map_search"),
    path('add_restaurant/', add_restaurant, name="add_restaurant"),
    path('add_menu_price/', add_menu_price, name="add_menu_price"),
    path('menu_search/', menu_search, name='menu_search'), 
    path('random_menu', random_menu, name = "random_menu")
]