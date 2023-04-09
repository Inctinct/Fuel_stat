from .models import RegistredUser
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import authenticate
from .models import Car, Fuel, Refueling, Firm, CheckFuel


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


class FirmSerializer(ModelSerializer):

    class Meta:
        model = Firm
        fields = '__all__'


class RefuelingSerializer(ModelSerializer):
    firm = FirmSerializer()

    class Meta:
        model = Refueling
        fields = '__all__'


class FuelSerializer(ModelSerializer):

    class Meta:
        model = Fuel
        fields = '__all__'


class CarSerializer(ModelSerializer):

    class Meta:
        model = Car
        fields = '__all__'


class CheckSerializer(serializers.Serializer):
    refueling = RefuelingSerializer()
    fuel = FuelSerializer()
    car = CarSerializer()
    number_of_liters = serializers.IntegerField()

    class Meta:
        model = CheckFuel
        fields = '__all__'


class CheckFuelSerializer(serializers.Serializer):
    checks = CheckSerializer(many=True)
    total_spent = serializers.SerializerMethodField()

    def get_total_spent(self, data):
        total_spent = 0
        for item in data.get('checks'):
            total_spent += item.number_of_liters * item.fuel.price

        return total_spent


class AverageSpeedSerializer(serializers.Serializer):
    car_number = serializers.CharField()
    average_speed = serializers.DecimalField(max_digits=10, decimal_places=2)


