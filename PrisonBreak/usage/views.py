from django.contrib.auth.models import User
from .models import UserProfile  # UserProfile 모델을 임포트합니다.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse


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
        security_question = request.POST['security_question']
        security_answer = request.POST['security_answer']
        
        # 새로운 사용자 생성
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            user.save()
            # User 객체와 함께 UserProfile 객체도 생성합니다.
            user_profile = UserProfile(user=user, security_question=security_question, security_answer=security_answer)
            user_profile.save()
            return redirect('user_login')
        else:
            return render(request, 'usage/createAccount.html', {'error': 'Username already exists'})
    else:
        return render(request, 'usage/createAccount.html')
    
def find_password(request):
    if request.method == "POST":
        # 사용자 입력 데이터 가져오기
        user_id = request.POST.get('id')
        security_question = request.POST.get('security-question')
        security_answer = request.POST.get('security-answer')
        
        # 해당 데이터와 일치하는 사용자 조회
        try:
            user = User.objects.get(
                id=user_id, 
                security_question=security_question, 
                security_answer=security_answer
            )
            # 비밀번호를 직접 알려주는 경우 (보안상 매우 위험)
            return HttpResponse(f'당신의 비밀번호는 {user.password}입니다.')
        except User.DoesNotExist:
            # 일치하는 사용자가 없는 경우
            return HttpResponse('일치하는 사용자 정보가 없습니다.')
    else:
        # GET 요청인 경우, 폼을 다시 렌더링
        return render(request, 'usage/findPassword.html')