from django.contrib import admin
from django.urls import path, include, re_path
from .views import RegistrationView, LoginView, ActivationAccountView, FuelStatisticView, CarStatisticView


urlpatterns = [
    re_path(r'^register/', RegistrationView.as_view()),
    re_path(r'^login/', LoginView.as_view(), name='login'),
    path('activate/<slug:uidb64>/<slug:token>/', ActivationAccountView.as_view(), name='activate'),
    re_path(r'^stat/', FuelStatisticView.as_view()),
    path('car-stat/', CarStatisticView.as_view()),

]