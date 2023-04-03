from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import datetime, timedelta
from django.conf import settings
import jwt


class Firm(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Fuel(models.Model):
    name = models.CharField(max_length=15)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Refueling(models.Model):
    adress = models.TextField()
    firm = models.ForeignKey(Firm, on_delete=models.CASCADE)

    def __str__(self):
        return self.adress


class UserManager(BaseUserManager):
    def create_user(self, password, email, phone,
                    is_admin=False, is_staff=False,
                    is_active=False, is_superuser=False,
                    ):
        if not phone:
            raise ValueError('User must have phone')
        if not email:
            raise ValueError('User must have email')
        if not password:
            raise ValueError('User must have password')

        user = self.model(phone=phone)
        user.set_password(password)
        user.email = email
        user.is_admin = is_admin
        user.is_staff = is_staff
        user.is_active = is_active
        user.is_superuser = is_superuser
        user.save()

        return user

    def create_superuser(self, password, phone, email):
        if not phone:
            raise ValueError('User must have phone')
        if not email:
            raise ValueError('User must have email')
        if not password:
            raise ValueError('User must have password')

        user = self.create_user(password=password, email=email, phone=phone)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user


class RegistredUser(AbstractUser):
    username = None
    email = models.EmailField()
    phone = models.CharField(max_length=13, unique=True)
    tg = models.CharField(max_length=50, unique=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token


class Car(models.Model):
    user = models.ForeignKey(RegistredUser, on_delete=models.CASCADE)
    number = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.number


class CheckFuel(models.Model):
    refueling = models.ForeignKey(Refueling, null=True, on_delete=models.SET_NULL)
    fuel = models.ForeignKey(Fuel, null=True, on_delete=models.SET_NULL)
    number_of_liters = models.PositiveIntegerField()
    payment_date = models.DateTimeField(auto_now_add=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)


class GpsImitation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    fuel_sensor = models.PositiveIntegerField()
    odometer = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
