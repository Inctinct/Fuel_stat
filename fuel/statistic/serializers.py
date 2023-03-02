from .models import RegistredUser
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import authenticate


class RegistrationSerializer(ModelSerializer):
    password = serializers.CharField(
        max_length=100,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(
        max_length=255,
        read_only=True
    )

    class Meta:
        model = RegistredUser
        fields = ['phone', 'email', 'password', 'token']

    def create(self, validated_data):
        return RegistredUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13)
    password = serializers.CharField(max_length=100, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        phone = data.get('phone', None)
        password = data.get('password', None)

        if phone is None:
            raise serializers.ValidationError('Phone number is required to login')

        if password is None:
            raise serializers.ValidationError('Password number is required to login')

        user = authenticate(username=phone, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this phone and password was not found')

        if not user.is_active:
            raise serializers.ValidationError('This account was not verified')

        return {
            'phone': user.phone,
            'token': user.token
        }
