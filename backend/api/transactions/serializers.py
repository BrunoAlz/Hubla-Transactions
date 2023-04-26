from rest_framework import serializers
from .models import Contract
from rest_framework.fields import CurrentUserDefault


class ContractRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['upload']

    def create(self, validated_data):

        user = self.context.get('user')
        instance = Contract(upload=validated_data['upload'], creator=user)
        instance.save()
        return instance
