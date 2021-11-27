from django.urls import path
from .views import *


app_name="restaurants"

urlpatterns = [
    path('search/', map_search, name="map_search"),
]