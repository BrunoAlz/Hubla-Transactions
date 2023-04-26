from django.urls import path
from .views import (ContractRegisterView, ContractListView,
                    ContractDetailAPIView)


urlpatterns = [
    path('contract/', ContractRegisterView.as_view()),
    path('contract/list/', ContractListView.as_view()),
    path('contract/<int:pk>/', ContractDetailAPIView.as_view()),
]
