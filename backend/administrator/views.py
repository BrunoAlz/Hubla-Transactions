from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from common.serializers import UserSerializer
from common import api_exceptions


class RegisterUserView(APIView):
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
