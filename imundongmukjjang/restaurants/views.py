from django.shortcuts import render, redirect, get_object_or_404
import pandas as pd
from accounts.models import CustomUser
from .models import Big_Category, Restaurant, Category, Menu_Price
from pathlib import Path
import os
from .form import *
from django.utils import timezone
from imundongmukjjang.settings import KAKAO_APPKEY
import json
from django.contrib.auth.decorators import login_required

BASE_DIR = Path(__file__).resolve().parent.parent
filename = os.path.join(BASE_DIR, 'restaurants', 'restaurants.csv')
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        restaurant = Restaurant.objects.filter(owner__username=str(request.user))
        length = len(restaurant)
        user = CustomUser.objects.values("is_assured")
        if length > 0:
            restaurant = restaurant[0]
            return render(request, 'home.html', {'restaurant' : restaurant, 'len':length, 'assurance': user[0]['is_assured']})
        return render(request, 'home.html', {'restaurant' : restaurant, 'len':length, 'assurance': user[0]['is_assured']})
    return render(request, 'home.html')

def rest_page(request):
    return render(request, 'rest_input.html')

def menu_page(request):
    return render(request, 'menu_input.html')

def init_db(request):
    data = pd.read_csv(filename, encoding = 'utf-8')
    data.head()

    categories = data['카테고리']
    temp = []
    for row in categories:
        if row != 0 and row not in temp:
            temp.append(row)
            new_category = Category()
            new_category.name = row
            new_category.big_category = Big_Category.objects.get(id=1)
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
            menus = eval(getattr(row, '메뉴'))
            max_price, min_price = 0, 1000000
            new_rest.save()
            for menu in menus.keys():
                new_menu = Menu_Price()
                new_menu.menu = menu
                if menus[menu] != '':
                    price = int(str(menus[menu]).replace(',',''))
                else: price = 0
                new_menu.price = price
                if max_price < price: max_price = price
                if min_price > price: min_price = price
                new_menu.restaurant = new_rest
                new_menu.save()
            new_rest.max_price, new_rest.min_price = max_price, min_price
            new_rest.save()
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

def order_by_cost(request, keyword):
    #keyword = request.GET.get('keyword')
    restaurants = Menu_Price.objects.filter(menu__contains=keyword).prefetch_related("restaurant").order_by('price')
    restaurants_list = list(restaurants)
    data = []
    for rest in restaurants_list:
        if rest.restaurant not in data:
            data.append(rest.restaurant)
    return render(request, 'search.html', {'restaurants': data, 'keyword':keyword, 'KAKAO_APPKEY':KAKAO_APPKEY})


@login_required
def post_restaurant(request):
    form = RestaurantInput()
    return render(request, 'rest_input.html', {'form': form})

@login_required
def create_restaurant(request):
    form1 = RestaurantInput()
    form = RestaurantInput(request.POST)
    if form.is_valid():
        rest = form.save(commit=False)
        rest.owner = CustomUser.objects.get(id=request.user.id)
        rest.address = request.POST["sample4_roadAddress"] + request.POST["sample4_detailAddress"]
        if len(Restaurant.objects.filter(name=rest.name)) != 0:
            return render(request, "rest_input.html", {'form': form1, 'register': 'dup'})
        rest.save()
        return redirect('restaurants:detail', rest.id)
    return render(request, "rest_input.html", {'form': form1, 'register': 'wrong'})

@login_required
def put_restaurant(request, id):
    restaurant = Restaurant.objects.get(id=id)
    menus = Menu_Price.objects.filter(restaurant__id=id)
    ct = Category.objects.all()
    if restaurant.owner != None:
        if request.method == 'POST' and restaurant.owner.username == str(request.user):
            restaurant.name = request.POST["title"]
            restaurant.phone = request.POST["phone"]
            restaurant.category = Category.objects.get(name=request.POST["category"])
            restaurant.address = request.POST["sample4_roadAddress"] + request.POST["sample4_detailAddress"]
            restaurant.save() 
            return redirect('restaurants:detail', restaurant.id)
        elif request.method == 'POST' and restaurant.owner.username != str(request.user):
            return render(request, "update.html", {'restaurant':restaurant, 'register':'wrong', "ct": ct})
        else:
            return render(request, "update.html", {'restaurant':restaurant, "ct": ct})
    return render(request, "update.html", {'restaurant':restaurant, 'register':'wrong', "ct": ct})

def random_menu(request):
    random_selected = Menu_Price.objects.order_by("?").first()
    menu = random_selected.menu
    price = random_selected.price
    restaurant = random_selected.restaurant
    return render(request, 'random_menu.html', {'menu':menu, 'price':price, 'restaurant':restaurant})

# 메뉴 추가 가능하도록 해야 함.
# 메뉴 삭제 가능하도록
@login_required
def add_menu_price(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    menus = Menu_Price.objects.filter(restaurant__id=restaurant.id)
    print(restaurant.owner != None)
    if restaurant.owner != None:
        if request.method == 'POST' and restaurant.owner.username == str(request.user):
            new_menu = Menu_Price()
            new_menu.menu = request.POST["menu"]
            new_menu.restaurant = restaurant
            new_menu.price = request.POST['price']
            new_menu.save()
        return render(request, 'menu_input.html', {'restaurant':restaurant, 'menus':menus})
    return render(request, "update.html", {'restaurant':restaurant, 'register':'wrong'})

def menu_delete(request, menu_id):
    menu = Menu_Price.objects.get(id=menu_id)
    restaurant_id = menu.restaurant.id
    menu.delete()
    return redirect('restaurants:add_menu_price', restaurant_id)

def detail(request, id):
    restaurants = Restaurant.objects.filter(id=id).prefetch_related('owner')
    restaurant = restaurants[0]
    owned = False
    if restaurant.owner != None and request.user.is_authenticated:
        if restaurant.owner.username == str(request.user):
            owned = True
    menus = Menu_Price.objects.filter(restaurant__id=id)
    return render(request, 'detail.html', {'restaurant': restaurant, 'menus':menus, 'KAKAO_APPKEY':KAKAO_APPKEY, 'owned':owned})

