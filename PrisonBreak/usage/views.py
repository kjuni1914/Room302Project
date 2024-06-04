from django.contrib.auth.models import User
from .models import UserProfile, Seat  # UserProfile and Seat models are imported
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required(login_url='')
def seat(request):
    """
    View to render the seating layout for authenticated users.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered seating layout page with user seat information.
    """
    user = request.user
    user_seat = None
    if user.is_authenticated:
        user_seat = Seat.objects.filter(user=user).first()

    seats = Seat.objects.all()
    return render(request, 'usage/seats.html', {
        'seats': seats,
        'user_seat_number': user_seat.seat_number if user_seat else None
    })

@login_required
def update_seat_status(request):
    """
    View to update the status of a seat (use or end usage).

    Args:
        request: The HTTP request object containing seat_number, action, and usage_time.

    Returns:
        JsonResponse: A response indicating the success status and seat usage details.
    """
    seat_number = request.POST.get('seat_number')
    action = request.POST.get('action')
    usage_time = request.POST.get('usage_time')

    seat = Seat.objects.get(seat_number=seat_number)

    if action == "use":
        seat.is_used = True
        seat.user = request.user
        seat.start_time = timezone.now()
        seat.expected_duration = usage_time
    elif action == "end":
        seat.is_used = False
        seat.user = None
        seat.start_time = None
        seat.expected_duration = None

    seat.save()
    return JsonResponse({'status': 'success', 'is_used': seat.is_used, 'user_seat_number': seat.seat_number})

def index(request):
    """
    View to render the login page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered login page.
    """
    return render(request, 'usage/login.html')

def user_login(request):
    """
    View to handle user login.

    Args:
        request: The HTTP request object containing username and password.

    Returns:
        HttpResponse: The rendered login page with error message if login fails.
        HttpResponseRedirect: Redirects to the seat page if login is successful.
    """
    if request.method == 'POST':
        username = request.POST['id']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, 'usage/login.html', {'error': 'ID not found'})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/seat')
        else:
            return render(request, 'usage/login.html', {'error': 'Incorrect password'})
    else:
        return render(request, 'usage/login.html')

def create_account(request):
    """
    View to handle user account creation.

    Args:
        request: The HTTP request object containing user details and security question.

    Returns:
        HttpResponse: The rendered create account page with error message if account creation fails.
        HttpResponseRedirect: Redirects to the login page if account creation is successful.
    """
    if request.method == 'POST':
        username = request.POST['id']
        password = request.POST['password']
        reenter_password = request.POST['reenter_password']
        security_question = request.POST['security_question']
        security_answer = request.POST['security_answer']
        
        if password != reenter_password:
            return render(request, 'usage/createAccount.html', {'error': 'Passwords do not match'})
        
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            user.save()
            user_profile = UserProfile(user=user, security_question=security_question, security_answer=security_answer)
            user_profile.save()
            return redirect('/')
        else:
            return render(request, 'usage/createAccount.html', {'error': 'Username already exists'})
    else:
        return render(request, 'usage/createAccount.html')

def change_password(request):
    """
    View to handle password change based on security question and answer.

    Args:
        request: The HTTP request object containing user ID, security question, answer, and new password.

    Returns:
        HttpResponse: The rendered change password page with a message indicating success or failure.
        HttpResponseRedirect: Redirects to the login page if password change is successful.
    """
    if request.method == "POST":
        user_id = request.POST.get('id')
        security_question = request.POST.get('security-question')
        security_answer = request.POST.get('security-answer')
        new_password = request.POST.get('new_password')
        reenter_password = request.POST.get('reenter_password')
        
        if new_password != reenter_password:
            return render(request, 'usage/changePassword.html', {'message': 'Re-entered Passwords do not match'})
        
        try:
            user_profile = UserProfile.objects.get(
                user__username=user_id, 
                security_question=security_question, 
                security_answer=security_answer
            )
            
            user = user_profile.user
            user.set_password(new_password)
            user.save()
            
            return redirect('user_login')
        except UserProfile.DoesNotExist:
            return render(request, 'usage/changePassword.html', {'message': 'Something is incorrect!'})
    else:
        return render(request, 'usage/changePassword.html')

@login_required
def get_seat_info(request):
    """
    View to retrieve information about all seats and the user's seat.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: A response containing seat information and the user's seat number.
    """
    seats = Seat.objects.all()
    user_seat = Seat.objects.filter(user=request.user).first()
    seat_data = [
        {
            'seat_number': seat.seat_number,
            'is_used': seat.is_used,
            'user': seat.user.username if seat.user else None,
            'start_time': seat.start_time,
            'expected_duration': seat.expected_duration
        }
        for seat in seats
    ]
    return JsonResponse({'status': 'success', 'seats': seat_data, 'user_seat': user_seat.seat_number if user_seat else None})

@login_required
def change_seat(request):
    """
    View to handle changing the user's seat.

    Args:
        request: The HTTP request object containing the new seat number.

    Returns:
        JsonResponse: A response indicating the success status of the seat change.
    """
    new_seat_number = request.POST.get('new_seat_number')
    current_seat = Seat.objects.get(user=request.user)
    new_seat = Seat.objects.get(seat_number=new_seat_number)

    new_seat.is_used = True
    new_seat.user = request.user
    new_seat.start_time = current_seat.start_time
    new_seat.expected_duration = current_seat.expected_duration
    new_seat.save()

    current_seat.is_used = False
    current_seat.user = None
    current_seat.start_time = None
    current_seat.expected_duration = None
    current_seat.save()

    return JsonResponse({'status': 'success'})
