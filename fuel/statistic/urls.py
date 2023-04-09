from django.contrib import admin
from django.urls import path, include, re_path
from .views import RegistrationView, LoginView, ActivationAccountView, FuelStatisticView, \
    CarStatisticView, AverageSpeedView


urlpatterns = [
    re_path(r'^register/', RegistrationView.as_view(), name='register'),
    re_path(r'^login/', LoginView.as_view(), name='login'),
    path('activate/<slug:uidb64>/<slug:token>/', ActivationAccountView.as_view(), name='activate'),
    re_path(r'^stat/', FuelStatisticView.as_view(), name='fuel_statistic'),
    path('car-stat/', CarStatisticView.as_view(), name='car_stat'),
    re_path(r'^speed/', AverageSpeedView.as_view(), name='car_speed')

]