from random import randint


def fuel_imitation() -> int:
    fuel_value = randint(25, 40)

    return fuel_value


def odometer_imitation() -> int:
    odometer_value = randint(60, 120)

    return odometer_value


def refueling_imitation() -> int:
    fuel = randint(300, 500)

    return fuel
