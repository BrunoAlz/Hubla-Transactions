from django.contrib import admin
from django.urls import path, include
from .views import RegisterUserView, LoginUserAPIView

urlpatterns = [
    path('register/', RegisterUserView.as_view()),
    path('login/', LoginUserAPIView.as_view()),
]