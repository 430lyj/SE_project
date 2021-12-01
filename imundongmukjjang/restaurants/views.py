from django.shortcuts import render, redirect
import pandas as pd
from .models import Restaurant, Category, Menu_Price
from pathlib import Path
import os
from .form import *
from django.utils import timezone
from imundongmukjjang.settings import KAKAO_APPKEY
import json


BASE_DIR = Path(__file__).resolve().parent.parent
filename = os.path.join(BASE_DIR, 'restaurants', 'restaurants.csv')
# Create your views here.
def home(request):
    return render(request, 'home.html')

def rest_page(request):
    return render(request, 'rest_input.html')

def menu_page(request):
    return render(request, 'menu_input.html')

def init_db(request):
    #pandas read_csv로 불러오기
    data = pd.read_csv(filename, encoding = 'utf-8')
    data.head()

    categories = data['카테고리']
    temp = []
    for row in categories:
        if row != 0 and row not in temp:
            temp.append(row)
            new_category = Category()
            new_category.name = row
            new_category.save()

    for row in data.itertuples():
        status = getattr(row, '영업상태명')
        if status == "영업/정상":
            new_rest = Restaurant()
            new_rest.phone = getattr(row, '전화번호')
            new_rest.address = getattr(row, '도로명주소')
            new_rest.name = getattr(row, '사업장명')
            new_rest.rating = float(getattr(row, '별점'))
            category = getattr(row, '카테고리')
            new_rest.category = Category.objects.get(name=category)
            new_rest.save()
            menus = eval(getattr(row, '메뉴'))
            for menu in menus.keys():
                new_menu = Menu_Price()
                new_menu.menu = menu
                new_menu.price = menus[menu]
                new_menu.restaurant = new_rest
                new_menu.save()
    return redirect('home')

def map_search(request):
    keyword = request.GET.get('keyword')
    restaurants = Menu_Price.objects.filter(menu__contains=keyword).prefetch_related("restaurant")
    restaurants_list = list(restaurants)
    data = []
    for rest in restaurants_list:
        if rest.restaurant not in data:
            data.append(rest.restaurant)
    return render(request, 'search.html', {'restaurants': data, 'keyword':keyword, 'KAKAO_APPKEY':KAKAO_APPKEY})

def add_restaurant(request):
    if request.method == "POST":
        form = RestaurantInput(request.POST)
        if form.is_valid():
            rest = form.save(commit=False)
            rest.created_at = timezone.now()
            rest.updated_at = timezone.now()
            rest.save()
            return render(request, "rest_input.html", {'register': "reg"})
        else:
            return render(request, "rest_input.html", {'register': "dup"})
    elif request.method == "PUT":
        form = RestaurantInput(request.POST)
        if form.is_valid():
            rest = form.save(commit=False)
            rest.updated_at = timezone.now()
            rest.save()
            return render(request, "rest_input.html", {'register': "reg"})
        else:
            return render(request, "rest_input.html", {'register': "dup"})
    else:
        form = RestaurantInput()
        return render(request, "rest_input.html", {'form': form})

def add_menu_price(request):
    if request.method == "POST":
        form = MenuInput(request.POST)
        if form.is_valid():
            rest = form.save(commit=False)
            rest.save()
            return render(request, "menu_input.html", {'register': "reg"})
    elif request.method == "PUT":
        form = MenuInput(request.POST)
        if form.is_valid():
            rest = form.save(commit=False)
            rest.save()
            return render(request, "menu_input.html", {'register': "reg"})
    else:
        form = MenuInput()
        return render(request, "menu_input.html", {'form': form})

def menu_search(request):
    keyword = request.GET.get('keyword')
    restaurants = Menu_Price.objects.filter(menu__contains=keyword).prefetch_related("restaurant")
    restaurants_list = list(restaurants)
    data = []
    for rest in restaurants_list:
        if rest.restaurant not in data:
            data.append(rest.restaurant)
    return render(request, 'menu_search.html', {'restaurants': data, 'keyword':keyword})