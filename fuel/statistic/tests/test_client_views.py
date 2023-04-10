import pytest
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
import json


pytestmark = [pytest.mark.django_db]
EVERYTHING_EQUALS_NON_NONE = type('omnieq', (), {"__eq__": lambda x, y: y is not None})()


class ApiTest(APITestCase):
    # fixtures = ['statistic/tests/fixtures/fixture_fuelstatistic.json',
    #             'statistic/tests/fixtures/fixture_refueling.json',
    #             'statistic/tests/fixtures/fixture_fuel.json',
    #             'statistic/tests/fixtures/fixture_car.json',
    #             'statistic/tests/fixtures/fixture_firm.json',
    #             'statistic/tests/fixtures/fixture_registreduser.json']

    def setUp(self) -> None:
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
        self.token = 'Bearer ' + str(response.data['token'])

    def test_fuel_statistic(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        url = reverse('fuel_statistic')
        response = self.client.get(url)
        assert response.data == EVERYTHING_EQUALS_NON_NONE
        assert response.status_code == 200

    def test_car_statistic(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        url = 'http://127.0.0.1:8000/api/car-stat/?number=666'
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data == EVERYTHING_EQUALS_NON_NONE

    def test_car_speed(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        url = reverse('car_speed')
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data == EVERYTHING_EQUALS_NON_NONE
