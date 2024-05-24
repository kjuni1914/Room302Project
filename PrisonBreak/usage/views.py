from django.shortcuts import render

def seat(request):
    return render(request, 'usage/seats.html')
# Create your views here.
