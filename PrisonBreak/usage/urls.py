from django.urls import path
from . import views

urlpatterns = [
    path('seat/', views.seat, name='seat'),
    path('index/', views.index, name='index'),
    path('', views.user_login, name='user_login'),
]
