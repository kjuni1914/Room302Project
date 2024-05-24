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

        # 사용자 인증
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/seat')
        else:
            # 인증 실패 시 로그인 페이지로 다시 이동
            return render(request, 'usage/login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'usage/login.html')
    
def create_account(request):
    if request.method == 'POST':
        username = request.POST['id']
        password = request.POST['password']
        
        # 새로운 사용자 생성
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return redirect('user_login')
        else:
            return render(request, 'usage/createAccount.html', {'error': 'Username already exists'})
    else:
        return render(request, 'usage/createAccount.html')
    
def find_password(request):
    return render(request, 'usage/findPassword.html')