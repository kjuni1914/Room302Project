from django.urls import path
from . import views

urlpatterns = [
    path('', views.seat, name='seat'),
]
