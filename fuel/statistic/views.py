from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from .models import RegistredUser
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .serializers import RegistrationSerializer, LoginSerializer
# Create your views here.


class RegistrationView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = RegistrationSerializer

    def send_mail(self, user_id, domain):
        user = RegistredUser.objects.get(id=user_id)
        mail_subject = 'ACTIVATION LINK'
        message = render_to_string('account_activation_email.html',
                                   {
                                       'user': user,
                                       'domain': domain,
                                       'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                       'token': account_activation_token.make_token(user)
                                   })
        to_email = user.email
        send_mail(mail_subject, message, recipient_list=[to_email],
                  from_mail=settings.EMAIL_HOST_USER)

    def post(self, request):
        user = request.data.get('user')
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        current_site = get_current_site(request)
        self.send_mail(user.id, current_site)

        return Response(serializer.data)


class ActivationAccountView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, uidb64, token):
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

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)


