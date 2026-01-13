from django.urls import path
from . import views

app_name = 'calculator'

urlpatterns = [
    path('', views.home, name='home'),
    path('calculate/', views.calculate, name='calculate'),
    path('history/', views.history, name='history'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]