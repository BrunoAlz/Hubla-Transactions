import re
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    """
    This view allows the creation of users in the system.

    Methods:
        `validate_first_name(self, value):`
            Checks if the first_name has only letters, if it doesn't it
            raises a validation exception.

        `validate_last_name(self, value):`
            Checks if the last_name has only letters, if it doesn't it
            raises a validation exception.

        `validate_email(self, value):`
            Checks if the email is being used by another user, if so
            it raises a validation exception.

        `validate_password(self, value):`
            Checks if the password has more than 5 characters, if not,
            raises validation exception

        `create(self, validated_data):`
            It receives the validated data, and creates the user.
    """

    def validate_first_name(self, value):
        if not re.match("^[A-Za-z]+$", value):
            raise serializers.ValidationError(
                'The first name can only contain letters.')
        return value

    def validate_last_name(self, value):
        if not re.match("^[A-Za-z]+$", value):
            raise serializers.ValidationError(
                'The last name can only contain letters.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'This email address is already in use.')
        return value

    def validate_password(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                'Password must be 5 characters long.')
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
