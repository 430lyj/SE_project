from os import name
from django.urls import path
from .views import *

app_name="restaurants"

urlpatterns = [
    path('search/<int:sorted_id>/', map_search, name="map_search"),
    path('add_restaurant/', post_restaurant, name="post_restaurant"),
    path('create_restaurant/', create_restaurant, name="create_restaurant"),
    path('<int:restaurant_id>/add_menu_price/', add_menu_price, name="add_menu_price"),
    path('<int:id>/', detail, name='detail'),
    path('update_restaurant/', put_restaurant, name='put_restaurant'),
    path('<int:menu_id>/delete/', menu_delete, name='menu_delete'),
    path('random_menu/', random_menu, name="random_menu"),
    path('random_menu/detail/', random_menu_detail, name="random_menu_detail"),
    path('category/', category, name="category"),
    path('category_detail/<int:category_id>/<int:sorted_id>/', category_detail, name="category_detail"),
    path('lists/<int:sorted>/', rest_lists, name="rest_lists"),
]