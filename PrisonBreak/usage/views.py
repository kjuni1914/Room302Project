from django.contrib.auth.models import User
from .models import UserProfile  # UserProfile 모델을 임포트합니다.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from .models import Seat
from django.contrib.auth.decorators import login_required

@login_required(login_url='')
def seat(request):
    user = request.user
    user_seat = None
    if user.is_authenticated:
        user_seat = Seat.objects.filter(user=user).first()

    seats = Seat.objects.all()
    return render(request, 'usage/seats.html', {
        'seats': seats,
        'user_seat_number': user_seat.seat_number if user_seat else None
    })

def update_seat_status(request):
    if request.method == "POST":
        seat_number = request.POST.get("seat_number")
        action = request.POST.get("action")
        usage_time = request.POST.get("usage_time", 0)

        if action == "use" and Seat.objects.filter(user=request.user, is_used=True).exists():
            return JsonResponse({"status": "error", "message": "You are already using another seat."})

        seat = Seat.objects.get(seat_number=seat_number)

        if action == "end" and seat.user != request.user:
            return JsonResponse({"status": "error", "message": "This seat is not your seat."})

        if action == "use":
            seat.is_used = True
            seat.user = request.user
            seat.usage_time = usage_time
        else:
            seat.is_used = False
            seat.user = None
            seat.usage_time = 0
        seat.save()

        user_seat_number = None
        if request.user.is_authenticated:
            user_seat = Seat.objects.filter(user=request.user).first()
            user_seat_number = user_seat.seat_number if user_seat else None

        return JsonResponse({
            "status": "success",
            "seat_number": seat_number,
            "is_used": seat.is_used,
            "user_seat_number": user_seat_number
        })

    
def index(request):
    return render(request, 'usage/login.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['id']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, 'usage/login.html', {'error': 'ID not found'})

        # 사용자 인증
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/seat')
        else:
            # 비밀번호가 일치하지 않을 때
            return render(request, 'usage/login.html', {'error': 'Incorrect password'})
    else:
        return render(request, 'usage/login.html')

    
def create_account(request):
    if request.method == 'POST':
        username = request.POST['id']
        password = request.POST['password']
        reenter_password = request.POST['reenter_password']
        security_question = request.POST['security_question']
        security_answer = request.POST['security_answer']
        
        # 비밀번호 재확인 검사
        if password != reenter_password:
            return render(request, 'usage/createAccount.html', {'error': 'Passwords do not match'})
        
        # 새로운 사용자 생성
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            user.save()
            # User 객체와 함께 UserProfile 객체도 생성합니다.
            user_profile = UserProfile(user=user, security_question=security_question, security_answer=security_answer)
            user_profile.save()
            return redirect('/')
        else:
            return render(request, 'usage/createAccount.html', {'error': 'Username already exists'})
    else:
        return render(request, 'usage/createAccount.html')
    
def change_password(request):
    if request.method == "POST":
        # 사용자 입력 데이터 가져오기
        user_id = request.POST.get('id')
        security_question = request.POST.get('security-question')
        security_answer = request.POST.get('security-answer')
        new_password = request.POST.get('new_password')
        reenter_password = request.POST.get('reenter_password')
        
        # 새로운 비밀번호와 재입력한 비밀번호 일치 여부 확인
        if new_password != reenter_password:
            return HttpResponse('재입력한 비밀번호가 일치하지 않습니다.')
        
        # 해당 데이터와 일치하는 사용자 조회
        try:
            user_profile = UserProfile.objects.get(
                user__username=user_id, 
                security_question=security_question, 
                security_answer=security_answer
            )
            
            # 사용자의 비밀번호 업데이트
            user = user_profile.user
            user.set_password(new_password)
            user.save()
            
            return HttpResponse('비밀번호가 성공적으로 변경되었습니다.')
        except UserProfile.DoesNotExist:
            # 일치하는 사용자가 없는 경우
            return HttpResponse('일치하는 사용자 정보가 없습니다.')
    else:
        # GET 요청인 경우, 폼을 다시 렌더링
        return render(request, 'usage/changePassword.html')
