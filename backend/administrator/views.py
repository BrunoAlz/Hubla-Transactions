from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from common.serializers import UserSerializer


class RegisterUserView(APIView):
    def post(self, request):
        #validando os dados do registro
        data = request.data
        # compara se os passwords são iguais
        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Passwords do not match!')
        
        return Response('ok')
