from django.contrib import admin
from .models import Fuel, Refueling, Firm, CheckFuel, RegistredUser, Car
# Register your models here.


class RegistredUserAdmin(admin.ModelAdmin):
    list_display = ['phone', 'email', 'is_active', 'tg']
    search_fields = ['phone', 'email', 'tg']


class FuelAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    search_fields = ['name', ]


class FirmAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name', ]


class RefuelingAdmin(admin.ModelAdmin):
    list_display = ['adress', ]
    search_fields = ['adress', ]


class CarAdmin(admin.ModelAdmin):
    list_display = ['user', 'number']
    search_fields = ['user', 'number']


class CheckFuelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CheckFuel._meta.get_fields()]
    search_fields = ['car__number', 'car__user']


admin.site.register(Firm, FirmAdmin)
admin.site.register(Fuel, FuelAdmin)
admin.site.register(Refueling, RefuelingAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(CheckFuel, CheckFuelAdmin)
admin.site.register(RegistredUser, RegistredUserAdmin)
