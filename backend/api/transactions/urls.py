from django.urls import path
from .views import ContractRegisterView, ContractListView

urlpatterns = [
    path('contract/', ContractRegisterView.as_view()),
    path('contract/list/', ContractListView.as_view()),
    # path('user/', AuthenticatedUserAPIView.as_view()),
]
