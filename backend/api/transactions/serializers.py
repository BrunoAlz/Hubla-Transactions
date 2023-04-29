from rest_framework import serializers
from .models import Contract, Transaction
import os


class ContractRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['upload']

    def validate(self, data):
        if not data.get('upload'):
            raise serializers.ValidationError(
                {'error': 'Você deve enviar um documento'})

        file_extension = os.path.splitext(data['upload'].name)[1]
        if file_extension.lower() != '.txt':
            raise serializers.ValidationError(
                {'error': 'Apenas arquivos .txt são aceitos.'})

        return data

    def create(self, validated_data):
        user = self.context.get('user')
        instance = Contract(upload=validated_data['upload'], creator=user)
        instance.save()
        return instance


class ContractListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['id', 'creator', 'created_at', 'upload']


class ContractTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'type', 'contract',
                  'date', 'product', 'price', 'seller']


class ContractDetailSerializer(serializers.ModelSerializer):
    transactio_contract = ContractTransactionsSerializer(many=True)

    class Meta:
        model = Contract
        fields = ['creator', 'created_at', 'upload', 'transactio_contract']
