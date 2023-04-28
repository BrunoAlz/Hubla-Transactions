from rest_framework import serializers
from core.models import User


class UserSerializer(serializers.ModelSerializer):
    """
        Serializa os dados do usuário. # TODO, COMENTAR DEPOIS
        COMENTAR OS MÉTODOS
    """

    def validate_first_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError(
                'O primeiro nome só pode conter letras.')
        return value

    def validate_last_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError(
                'O último nome só pode conter letras.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Este endereço de e-mail já está em uso.')
        return value

    def validate_password(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                'A senha deve ter pelo menos 5 caracteres.')
        return value

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
