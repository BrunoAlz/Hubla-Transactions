from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from core.models import User
from common.serializers import UserSerializer
from common import api_exceptions
from rest_framework import status
from .authentication import JWTAuthentucation

# Refatorar para convenção do DRF
class RegisterUserView(APIView):
    """
    Esta view permite a criação de usuários no sistema.
    """
    def post(self, request):
        #validando os dados do registro
        data = request.data
        # compara se os passwords são iguais
        if data['password'] != data['password_confirm']:
            # Criando Exceções customizadas
            raise api_exceptions.PasswordDoNotMatchException()
        

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Validações OK - Tem que testar, Registrando usuário e retornando dados.
        return Response(serializer.data)


class LoginUserAPIView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        # Verifica se o usuário está correto / existe
        if user is None:
            raise exceptions.AuthenticationFailed({'error': 'Please, verify your data input'})
        
        # Verifica se o pass está correto / existe
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed({'error': 'Please, verify your data input'})        
    

        # Instancia a Classe geradora de Tokens JWT
        jwt_authentication = JWTAuthentucation()
        # Chama o método que Cria o Token, passando o Id do usuário da Requisição
        token =jwt_authentication.generate_jwt(user.id) 
        # PADRONIZAR AS RESPOSTAS PARA QUE FIQUEM ASSIM
        return Response([ 
                    {
                        'message': 'success', 
                        # Retornando o Token no Login
                        'token': token,
                        'user': UserSerializer(user).data
                    }
                ], status=status.HTTP_200_OK )

