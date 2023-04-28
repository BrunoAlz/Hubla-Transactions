from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from core.models import User
from core.serializers import UserSerializer
from core import api_exceptions
from rest_framework import status
from .authentication import JWTAuthentucation
from rest_framework import permissions

# Refatorar para convenção do DRF


class RegisterUserView(APIView):
    """
    Esta view permite a criação de usuários no sistema.
    """

    def post(self, request):
        # Recebe os dados do Serializer
        serializer = UserSerializer(data=request.data)
        # Verifica se os dados estão validos
        if serializer.is_valid():
            # Se sim salva os dados
            serializer.save()
            # Retorna os dados
            return Response({"success": "User registred!"}, status=status.HTTP_200_OK)
        else:
            # Se não Retorna os erros, e o status.
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserAPIView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        # Verifica se o usuário está correto / existe
        if user is None:
            raise exceptions.AuthenticationFailed(
                {'error': 'Please check your credentials!'})

        # Verifica se o pass está correto / existe
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed(
                {'error': 'Please check your credentials!'})

        # Chama o método ESTATICO que Cria o Token, passando o Id do usuário da Requisição
        token = JWTAuthentucation.generate_jwt(user.id)
        # PADRONIZAR AS RESPOSTAS PARA QUE FIQUEM ASSIM
        return Response([{'user': UserSerializer(user).data, 'token': token}], status=status.HTTP_200_OK)


class AuthenticatedUserAPIView(APIView):

    authentication_classes = [JWTAuthentucation]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
