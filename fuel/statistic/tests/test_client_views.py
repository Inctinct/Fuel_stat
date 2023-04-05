import pytest
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
import json


pytestmark = [pytest.mark.django_db]
EVERYTHING_EQUALS_NON_NONE = type('omnieq', (), {"__eq__": lambda x, y: y is not None})()


class ApiTest(APITestCase):

    def setUp(self) -> None:
        password = make_password('passw12345')
        self.user = get_user_model().objects.create(
            email='test@test.com',
            password=password,
            phone='12345',
            is_active=True
        )

        url = reverse('login')
        data = {
            'email': self.user.email,
            'phone': self.user.phone,
            'password': 'passw12345',
        }
        json_data = json.dumps(data)
        self.token = 'Bearer ' + str(
            self.client.post(url,
                             data=json_data,
                             content_type='application/json').data['token'])[2:-1]
