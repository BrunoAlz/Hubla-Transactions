from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from core.models import User
from core.serializers import UserSerializer
from core import api_exceptions
from rest_framework import status
from administrator.authentication import JWTAuthentucation
from rest_framework import permissions

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

        # serializer = UserSerializer(data=data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()

        # Validações OK - Tem que testar, Registrando usuário e retornando dados.
        return Response(data)
