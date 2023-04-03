from celery import shared_task
from django.utils.http import urlsafe_base64_encode

from .models import RegistredUser, Car, GpsImitation, CheckFuel
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.mail import send_mail
from .imitation import fuel_imitation, odometer_imitation, refueling_imitation


@shared_task()
def send_activation_mail(user_id, domain):
    user = RegistredUser.objects.get(id=user_id)
    mail_subject = "ACTIVATION LINK"
    message = render_to_string('account_activation_email.html',
                               {
                                   "user": user,
                                   "domain": domain,
                                   "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                                   "token": account_activation_token.make_token(user)
                               })
    to_email = user.email
    is_sent = send_mail(mail_subject, message, recipient_list=[to_email],
              from_email=settings.EMAIL_HOST_USER)

    return is_sent


@shared_task()
def gps_imitation():
    cars = Car.objects.all()

    for car in cars:
        gps = GpsImitation.objects.filter(car=car).order_by('-id')[:1]
        GpsImitation.objects.create(car=car, fuel_sensor=fuel_imitation(),
                                    odometer=odometer_imitation(gps.odometer))


@shared_task()
def check_imitation():
    cars = Car.objects.all()

    for car in cars:
        test = CheckFuel.objects.first()
        CheckFuel.objects.create(car=car, refueling=test.refueling,
                                 fuel=test.fuel, number_of_liters=refueling_imitation())



