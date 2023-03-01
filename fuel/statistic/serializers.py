from .models import RegistredUser
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


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
        fields = ['phone', 'email', 'password', 'tg', 'token']

    def create(self, validated_data):
        return RegistredUser.objects.create_user(**validated_data)