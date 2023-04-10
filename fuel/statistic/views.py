from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.mail import send_mail
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from .models import RegistredUser, CheckFuel, Firm, GpsImitation, Car
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .serializers import RegistrationSerializer, LoginSerializer, CheckFuelSerializer, AverageSpeedSerializer
from django.db.models import F
from .tasks import send_activation_mail
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
# Create your views here.


class RegistrationView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(
        request_body=RegistrationSerializer,
        request_method='POST',
        responses={
            200: RegistrationSerializer
        }
    )
    def post(self, request):
        """
        create non-active account and send activation mail
        """
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        current_site = get_current_site(request)
        send_activation_mail.delay(user.id, str(current_site))

        return Response(serializer.data)


class ActivationAccountView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, uidb64, token):
        """ activation account when clicking a link in an email"""
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = RegistredUser.objects.get(id=uid)
        except Exception as e:
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response('Thank you for email confirmation!')
        return Response('Somethong wrong with your account', status=403)


class LoginView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        request_body=LoginSerializer,
        request_method='POST',
        responses={
            200: LoginSerializer
        }
    )
    def post(self, request):
        """login account and create to use some views with permissions"""
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)


class FuelStatisticView(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(
        request_method="GET",
        responses={
            200: CheckFuelSerializer
        }
    )
    def get(self, request):
        """get statistic for all cars user with total spent money for fuel"""
        check = {}
        now = datetime.now()
        user = request.user
        check['checks'] = CheckFuel.objects.filter(car__user=user, payment_date__month=now.month)

        serializer = CheckFuelSerializer(check)

        return Response(serializer.data)


class CarStatisticView(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(
        request_mehtod='GET',
        responses={
            200: CheckFuelSerializer
        }
    )
    def get(self, request):
        """get  statistic for input cars numbers within month period"""
        now = datetime.now()
        user = request.user
        car_numbers = request.GET.get('number')
        list_id = []
        for car_number in car_numbers.split(','):

            checks = CheckFuel.objects.filter(car__number=car_number, car__user=user,
                                              payment_date__month=now.month).values_list('id', flat=True)
            list_id.extend(checks)
        check = (CheckFuel.objects.filter(car__user=user).in_bulk(list_id)).values()
        print(check)
        serializer = CheckFuelSerializer({'checks': check})

        return Response(serializer.data)


class AverageSpeedView(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(
        request_method='GET',
        responses={
            200: AverageSpeedSerializer
        }

    )
    def get(self, request):
        """calculate the average speed of the user's machines based on the data sent"""
        now = datetime.now()
        serializer_dict = {}
        user = request.user
        cars = set(GpsImitation.objects.filter(car__user=user,
                                               created_at__month=now.month).values_list('car', flat=True))
        for car in cars:
            car_speed = {}
            odometer = list(GpsImitation.objects.filter(car__id=car).values_list('odometer', flat=True))
            odometer_sum = sum(odometer)
            average_speed = odometer_sum / len(odometer)
            car_number = Car.objects.filter(id=car).values_list('number', flat=True)
            car_speed['car_number'] = car_number[0]
            car_speed['average_speed'] = average_speed
            serializer_dict[car] = car_speed
        serializer = AverageSpeedSerializer(serializer_dict.values(), many=True)

        return Response(serializer.data)




