from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (ContractRegisterSerializer,
                          ContractListSerializer, ContractDetailSerializer)
from user.authentication import JWTAuthentucation
from rest_framework import permissions
from .models import Contract
from rest_framework import serializers


# Refatorar para convenção do DRF


class ContractRegisterView(APIView):
    """
    A view for registering a contract.

    `Attributes`:
        authentication_classes (list): A list of authentication classes 
        used for this view.
        permission_classes (list): A list of permission classes used for 
        this view.


    `Returns`:
        A Response object containing a success message if the contract 
        was created successfully,
        or an error message if the request data is invalid.

    """
    authentication_classes = [JWTAuthentucation]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        serializer = ContractRegisterSerializer(
            data=request.data, context={'user': request.user})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'success': 'Successfully registered contract'})

        except serializers.ValidationError as e:
            return Response({'error': e.detail})


class ContractListView(APIView):
    """
    This view shows contracts created by the user,
    each user can only see their own data.

    `Returns:`
            A Response object containing a list of serialized
            Contract objects created by the authenticated user.
    """
    authentication_classes = [JWTAuthentucation]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user.id
        contracts = Contract.objects.filter(creator_id=user)
        serializer = ContractListSerializer(contracts, many=True)
        return Response(serializer.data)


class ContractDetailAPIView(APIView):
    """
    This view will search for transactions related to the contract
    created by the user. After uploading the contract, the system
    will wait for the file to be processed asynchronously, as soon
    as it is processed, it will be possible to view all transactions
    related to the contract.


    `Args:`
        pk (int): The primary key of the contract

    `Returns:`
    A Response object containing a serialized ContractDetail
    object `if the contract exists and belongs to
    the authenticated user`, or an error message.
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
