from random import randint



def fuel_imitation():
    fuel_value = randint(25, 40)

    return fuel_value


def odometer_imitation(odometer):
    odometer_value = odometer + randint(60, 120)

    return odometer_value


def refueling_imitation():
    fuel = randint(300, 500)
    return fuel