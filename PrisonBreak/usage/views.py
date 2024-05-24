from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def seat(request):
    return render(request, 'usage/seats.html')
# Create your views here.

def index(request):
    return render(request, 'usage/login.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['id']
        password = request.POST['password']
        # 학교 이메일 도메인 확인
        
        user = User.objects.create_user(username=username, password=password)
        user.save()
            # 사용자 로그인 후 리다이렉트
        login(request, user)
        return redirect('index')
        
    else:
        return render(request, 'usage/login.html')
    
def create_account(request):
    return render(request, 'usage/createAccount.html')