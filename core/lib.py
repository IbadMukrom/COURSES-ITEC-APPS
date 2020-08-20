import random
from django.contrib.auth.models import User


def useracak():
    range_start = 10**(5-1)
    range_end = (10**5)-1
    angka = random.randint(range_start, range_end)

    return angka