from django.conf import settings
from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor
from aiogram.utils.markdown import text, bold
from django.core.management.base import BaseCommand
from aiogram.types import ParseMode, ChatActions
from asgiref.sync import sync_to_async
import logging
import asyncio
from ...models import CheckFuel, GpsImitation
from datetime import datetime
from prettytable import PrettyTable


logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.TELEGRAMBOT_API_TOKEN)

dp = Dispatcher(bot)

button = KeyboardButton('Statistic')


keyboard = ReplyKeyboardMarkup()

keyboard.add(button)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer("Hello", reply_markup=keyboard)


@sync_to_async()
def get_statistic(user_number: int):
    """"
    calculation of analytics by sensors and the formation
    of this data in a file with the possibility of sending it to the user
    """
    stat = PrettyTable()
    stat.field_names = ["Fuel sensor", "Odometer", "Refueling liters",
                        "Lack of fuel", "Fuel consumption", "Expected flow fuel"]
    now = datetime.now()
    average_fuel_consumption = 30
    cars_id = set(CheckFuel.objects.filter(
        car__user__phone=user_number, payment_date__month=str(now.month)).values_list('car', flat=True))
    for car_id in cars_id:
        fuel_sensor = sum(list(GpsImitation.objects.filter(
            car__id=car_id, created_at__month=str(now.month)).values_list('fuel_sensor', flat=True)))
        odometer = sum(list(GpsImitation.objects.filter(
            car__id=car_id, created_at__month=str(now.month)).values_list('odometer', flat=True)))
        refueling_liters = sum(list(CheckFuel.objects.filter(
            car__id=car_id, payment_date__month=str(now.month)).values_list('number_of_liters', flat=True)))
        lack_of_fuel = refueling_liters - fuel_sensor
        fuel_consumption = fuel_sensor / (odometer / 100)
        expected_flow_fuel = (odometer / 100) * average_fuel_consumption
        stat.add_row([fuel_sensor, odometer, refueling_liters, lack_of_fuel, fuel_consumption, expected_flow_fuel])
    with open('stat.txt', 'w') as fp:
        table = stat.get_string()
        fp.write(table)
        fp.write('\n')


@dp.message_handler(state='*', commands=['statistic'])
async def statistic(msg: types.Message):
    """request to generate analytics by phone number"""
    user_number = msg.get_args()
    await get_statistic(user_number)
    await msg.reply_document(open('stat.txt', 'rb'))


@dp.message_handler(lambda message: message.text == 'Statistic')
async def statistic_info(msg: types.Message):
    msg_to_answer = "to get statistics, enter the /statistic command and the user's phone number"
    await bot.send_message(msg.from_user.id, msg_to_answer)


class Command(BaseCommand):
    help = 'Test TG Bot'

    def handle(self, *args, **options):
        executor.start_polling(dp)