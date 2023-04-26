from django.urls import path
from .views import ContractRegisterView

urlpatterns = [
    path('contract/', ContractRegisterView.as_view()),
    # path('login/', LoginUserAPIView.as_view()),
    # path('user/', AuthenticatedUserAPIView.as_view()),
]
