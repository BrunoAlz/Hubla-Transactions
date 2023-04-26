from django.urls import path
from .views import (RegisterUserView, LoginUserAPIView,
                    AuthenticatedUserAPIView)

urlpatterns = [
    path('register/', RegisterUserView.as_view()),
    path('login/', LoginUserAPIView.as_view()),
    path('user/', AuthenticatedUserAPIView.as_view()),
]
