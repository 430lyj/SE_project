from os import name
from django.urls import path
from .views import *

app_name="restaurants"

urlpatterns = [
    path('search/', map_search, name="map_search"),
    path('add_restaurant/', post_restaurant, name="post_restaurant"),
    path('create_restaurant/', create_restaurant, name="create_restaurant"),
    path('<int:restaurant_id>/add_menu_price/', add_menu_price, name="add_menu_price"),
    path('<int:id>/', detail, name='detail'),
    path('<int:id>/update/', put_restaurant, name='put_restaurant'),
    path('<int:menu_id>/delete/', menu_delete, name='menu_delete'),
    path('random_menu', random_menu, name = "random_menu")
]