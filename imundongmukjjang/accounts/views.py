from django.contrib.auth.models import UserManager
from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.


def signup(request):
    if request.method == "POST":
        try:
            if CustomUser.objects.filter(username = request.POST['username']).exists(): # 이미 등록된 회원일 경우
                return render(request, "signup.html", {"validity": 0})
            elif request.POST["password1"] == request.POST["password2"]:    # 회원가입 정상 진행
                user = CustomUser.objects.create_user(
                    username=request.POST["username"], password=request.POST["password1"], biz_registration=request.FILES["uploadedFile"])
                auth.login(request, user)
                return redirect('home')
            else:
                return render(request, "signup.html", {"validity": 1})  # 입력한 비밀번호 두 개가 일치하지 않을 경우
        except Exception as e:
            print(e)
            return render(request, "signup.html", {"filled": 0})
    return render(request, 'signup.html')


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'signin.html', {"validity": 1})
    else:
        return render(request, 'signin.html')

def logout(request):
    auth.logout(request)
    return redirect('home')

@login_required
def mypage(request):
    return render(request, 'mypage.html')