from django.urls import path
from . import views

urlpatterns = [
    path('seat/', views.seat, name='seat'),
    path('update_seat_status/', views.update_seat_status, name='update_seat_status'),
    path('', views.user_login, name='user_login'),
    path('index/', views.index, name='index'),
    path('changePassword/', views.change_password, name='change_password'),
    path('createAccount/',views.create_account, name='create_account')

]
