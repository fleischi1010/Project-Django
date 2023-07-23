# weather/urls.py
from django.urls import path
from . import views
from .views import index

urlpatterns = [
    path('', index, name='index'),
    path('weather/<str:city>/', views.weather_detail, name='weather_detail'),
    path('save_city/', views.save_city, name='save_city'),
    path('register/', views.register, name='register'),
    path('user_city/', views.user_city, name='user_city'),
]