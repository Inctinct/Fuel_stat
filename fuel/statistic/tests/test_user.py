import pytest
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
import json


pytestmark = [pytest.mark.django_db]


class ApiTest(APITestCase):
    def test_register_user(self):
        payload = dict(
            email="test@test.com",
            password="123456789",
            phone="12345",
            is_active=True
        )
        url = reverse('register')
        response = self.client.post(url, payload)
        data = response.data
        assert data["email"] == payload["email"]
        assert data["phone"] == payload["phone"]

    def test_login_user(self):
        password = make_password('passw12345')
        self.user = get_user_model().objects.create(
            email='test@test.com',
            password=password,
            phone='12345',
            is_active=True
        )

        url = reverse('login')
        data = {'user': {
            'phone': self.user.phone,
            'password': 'passw12345',
        }}
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        assert response.status_code == 200
