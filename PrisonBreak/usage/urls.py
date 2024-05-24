from django.urls import path
from . import views

urlpatterns = [
    path('', views.seat, name='seat'),
    path('', views.index, name='index'),
    path('login/', views.user_login, name='user_login'),
    path('createAccount/',views.create_account, name='create_account')
]
