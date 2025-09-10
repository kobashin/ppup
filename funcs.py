from datetime import datetime
import random


def getWeekday(year, month, day):
    dt = datetime(year=year, month=month, day=day)
    return dt.weekday()


def getLastDay(year, month):
    if month == 12:
        return 31
    else:
        return (datetime(year, month + 1, 1) - datetime(year, month, 1)).days


def getRandomInt(min, max):
    return random.randint(min, max)
