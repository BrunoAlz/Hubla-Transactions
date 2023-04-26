from rest_framework import serializers
from .models import Contract


class ContractRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['upload']

    def create(self, validated_data):

        user = self.context.get('user')
        instance = Contract(upload=validated_data['upload'], creator=user)
        instance.save()
        return instance


class ContractListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['creator', 'created_at', 'upload']


# class ContractTransactionDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transactions
#         fields = ['campo1', 'campo2', ...]

class ContractDetailSerializer(serializers.ModelSerializer):
    # dados_relacionados = ContractTransactionSerializer(many=True)
    # 'dados_relacionados' Colocar nos Fields depois
    class Meta:
        model = Contract
        fields = ['creator', 'created_at', 'upload']
