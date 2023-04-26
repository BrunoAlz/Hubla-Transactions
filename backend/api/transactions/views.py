from rest_framework.views import APIView
from rest_framework.response import Response
from core.api_permissions import IsOwnerOrRedirect
from core.models import User
from .serializers import ContractRegisterSerializer, ContractListSerializer, ContractDetailSerializer
from administrator.authentication import JWTAuthentucation
from rest_framework import permissions
from rest_framework import exceptions
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
        contracts = Contract.objects.filter(creator_id=user)
        serializer = ContractListSerializer(contracts, many=True)
        return Response(serializer.data)


class ContractDetailAPIView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    authentication_classes = [JWTAuthentucation]
    permission_classes = [IsOwnerOrRedirect]

    def get_object(self, pk):
        try:
            contract = Contract.objects.get(
                pk=pk, creator_id=self.request.user)

            self.check_object_permissions(self.request, contract)
            return contract
        except Contract.DoesNotExist:
            raise exceptions.NotFound(
                {'error': 'That contract do not exists or it doesnt belows to you'})

    def get(self, request, pk, format=None):
        contract = self.get_object(pk)
        # faz a relação entre os models
        # dados_relacionados = seu_modelo.modelo_relacionado.all()
        # E serializar os dados usando o seu serializador
        serializer = ContractDetailSerializer(contract)
        # retorna
        return Response(serializer.data)
