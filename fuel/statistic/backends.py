import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import RegistredUser


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        request.user = None
        auth_header = authentication.get_authorization_header(request).decode('utf-8')

        if not auth_header:
            return None

        auth_header_token = auth_header.split(" ")
        if len(auth_header_token) < 2:
            return None

        token = auth_header_token[1]
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except Exception as e:
            msg = f'Authentication Error. Unable to decode token {e} {token=}'
            raise  exceptions.AuthenticationFailed(msg)
        try:
            user = RegistredUser.objects.get(id=payload['id'])
        except Exception as e:
            msg = 'The user corresponding to the given token was not found.'
            raise exceptions.AuthenticationFailed(msg)
        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)

        return user, token