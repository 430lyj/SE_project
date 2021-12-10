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
from django.core.paginator import Paginator

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

def map_search(request, sorted_id):
    keyword = request.GET.get('keyword')
    if keyword != None:
        restaurants = Menu_Price.objects.filter(menu__contains=keyword).prefetch_related("restaurant").order_by('-restaurant__rating')
        if sorted_id == 1:
            restaurants = restaurants.order_by('restaurant__min_price')
        if sorted_id == 2:
            restaurants = restaurants.order_by('-restaurant__rating')
        restaurants_list = list(restaurants)
        data = []
        for rest in restaurants_list:
            if rest.restaurant not in data:
                data.append(rest.restaurant)
        return render(request, 'search.html', {'restaurants': data, 'keyword':keyword, 'KAKAO_APPKEY':KAKAO_APPKEY, 'sorted_id':sorted_id})
    return render(request, 'search.html', {'keyword':keyword, 'sorted_id':sorted_id})
    

@login_required
def post_restaurant(request):
    categories = Category.objects.all().order_by('name')
    if Restaurant.objects.filter(owner__username=str(request.user)).exists():
        rest = Restaurant.objects.filter(owner__username=str(request.user))
        return render(request, "rest_input.html", {'register': 'exist'})
    return render(request, 'rest_input.html', {'categories':categories})

@login_required
def create_restaurant(request):
    try:
        categories = Category.objects.all().order_by('name')
        user = CustomUser.objects.get(username=str(request.user))
        user.biz_registration = request.FILES["uploadedFile"]
        new_restaurant = Restaurant()
        new_restaurant.name = request.POST['name']
        if len(Restaurant.objects.filter(name=request.POST['name'])) != 0:
            return render(request, "rest_input.html", {'register': 'dup'})
        new_restaurant.phone = request.POST['phone']
        new_restaurant.category = Category.objects.get(id=int(request.POST['category']))
        new_restaurant.owner = CustomUser.objects.get(username=str(request.user))
        new_restaurant.address = request.POST["sample4_roadAddress"] + request.POST["sample4_detailAddress"]
        new_restaurant.save()
        return redirect('restaurants:detail', new_restaurant.id)
    except Exception as e:
        print(e)
        return render(request, "rest_input.html", {'register': 'wrong', 'categories':categories})

@login_required
def put_restaurant(request):
    try:
        restaurants = Restaurant.objects.filter(owner__username=str(request.user))
        ct = Category.objects.all().order_by('name')
        if restaurants.exists():
            restaurant = restaurants[0]
            if request.method == 'POST':
                menus = Menu_Price.objects.filter(restaurant=restaurant)
                restaurant.name = request.POST["title"]
                restaurant.phone = request.POST["phone"]
                restaurant.category = Category.objects.get(id=int(request.POST['category']))
                restaurant.address = request.POST["sample4_roadAddress"] + request.POST["sample4_detailAddress"]
                restaurant.save() 
                return redirect('restaurants:detail', restaurant.id)
            else:
                return render(request, "update.html", {'restaurant':restaurant, "ct": ct})
        return redirect('restaurants:post_restaurant')
    except Exception as e:
        print(e)
        return render(request, "update.html", {'restaurants':restaurants, 'register':'wrong', "ct": ct})

def random_menu(request):
    return render(request, 'random_menu.html')

def random_menu_detail(request):
    #가격이 0원이 아니고 None이 아닌 메뉴가 골라질 때까지 반복
    while True:
        random_selected = Menu_Price.objects.order_by("?").first()
        menu = random_selected.menu
        price = random_selected.price
        restaurant = random_selected.restaurant
        #가격이 0원이 아니고 None이 아니면 반복문 탈출
        if price !=0 and price != None:
            break
    return render(request, 'random_menu_detail.html', {'menu':menu, 'price':price, 'restaurant':restaurant})

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
    menus = Menu_Price.objects.filter(restaurant__id=id)
    return render(request, 'detail.html', {'restaurant': restaurant, 'menus':menus, 'KAKAO_APPKEY':KAKAO_APPKEY})

def category(request):
    categories = Big_Category.objects.all()
    return render(request, 'category.html', {'categories':categories})

def category_detail(request, category_id, sorted_id):
    '''
    sorted_id 정의
    0 : 정렬 기준 없음
    1 : 최소 가격 기준 정렬
    2 : 평점 기준 정렬
    '''
    restaurants = Restaurant.objects.filter(category__big_category__id=category_id)
    if sorted_id == 1:
        restaurants = restaurants.order_by('min_price')
    elif sorted_id == 2:
        restaurants = restaurants.order_by('-rating')
    paginator = Paginator(restaurants, 10)
    page = request.GET.get('page')
    paginated_restaurants = paginator.get_page(page)
    return render(request, 'category_detail.html', {'restaurants':paginated_restaurants, 'KAKAO_APPKEY':KAKAO_APPKEY, 'category_id':category_id})
    
def rest_lists(request, restaurants, sorted):
    if sorted == 1:
        restaurants_list = restaurants.order_by('min_price')
    elif sorted == 2:
        restaurants_list = restaurants.order_by('rating')
    else: 
        restaurants_list = restaurants
    return render(request, 'rest_lists.html', {'restaurants':restaurants_list,'KAKAO_APPKEY':KAKAO_APPKEY})