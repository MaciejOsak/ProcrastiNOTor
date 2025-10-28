from exceptions import *


def assert_time_wasters(value):
    if value == "":
        raise NoWastersError
    if len(value.split(", ")) > 100:
        raise HugeWastersCountError


def assert_minute_limit(value):
    try:
        int(value)
    except (ValueError, TypeError):
        raise IncorrectTimeLimitTypeError
    if int(value) > 1440:
        raise HugeTimeLimitValueError
