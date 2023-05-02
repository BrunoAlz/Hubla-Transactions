from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (ContractRegisterSerializer,
                          ContractListSerializer, ContractDetailSerializer)
from user.authentication import JWTAuthentucation
from rest_framework import permissions
from rest_framework import exceptions
from .models import Contract
from rest_framework import serializers


# Refatorar para convenção do DRF


class ContractRegisterView(APIView):
    """
    Esta view permite a criação de usuários no sistema.
    """
    authentication_classes = [JWTAuthentucation]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # validando os dados do registro
        serializer = ContractRegisterSerializer(
            data=request.data, context={'user': request.user})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'success': 'Contrato registrado com sucesso.'})

        except serializers.ValidationError as e:
            return Response({'error': e.detail})


class ContractListView(APIView):

    authentication_classes = [JWTAuthentucation]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        user = request.user.id
        contracts = Contract.objects.filter(creator_id=user)
        serializer = ContractListSerializer(contracts, many=True)
        return Response(serializer.data)


class ContractDetailAPIView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    authentication_classes = [JWTAuthentucation]

    def get_object(self, pk):
        check = Contract.objects.filter(
            pk=pk, creator_id=self.request.user).exists()
        if check:
            contract = Contract.objects.get(
                pk=pk, creator_id=self.request.user)

            self.check_object_permissions(self.request, contract)

            return contract
        else:
            return None

    def get(self, request, pk, format=None):
        contract = self.get_object(pk)
        if contract is None:
            return Response({'error': 'That contract do not exists or it doesnt belows to you'})
        else:
            serializer = ContractDetailSerializer(contract)
            return Response(serializer.data)
