from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from core.models import User
from .serializers import ContractRegisterSerializer
from core import api_exceptions
from administrator.authentication import JWTAuthentucation
from rest_framework import permissions
from .models import Contract

# Refatorar para convenção do DRF


class ContractRegisterView(APIView):
    """
    Esta view permite a criação de usuários no sistema.
    """
    authentication_classes = [JWTAuthentucation]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # validando os dados do registro
        data = request.data

        serializer = ContractRegisterSerializer(
            data=data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Validações OK - Tem que testar, Registrando usuário e retornando dados.
        return Response(data)


class ContractListView(APIView):

    authentication_classes = [JWTAuthentucation]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        user = request.user.id
        print(user)
        contracts = Contract.objects.filter(creator_id=user)
        print(contracts)

        return Response("ok")
