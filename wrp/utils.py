import os
import sys
import time
import math
import datetime
from datetime import timedelta


def this_week_range():
    now = datetime.datetime.now()

    zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                          microseconds=now.microsecond)
    over_today = zero_today + datetime.timedelta(hours=23, minutes=59, seconds=59)

    this_week_start = zero_today - timedelta(days=now.weekday())
    this_week_end = over_today + timedelta(days=6 - now.weekday())

    return this_week_start, this_week_end


def next_week_range():
    now = datetime.datetime.now()
    zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                          microseconds=now.microsecond)
    over_today = zero_today + datetime.timedelta(hours=23, minutes=59, seconds=59)

    last_week_start = zero_today - timedelta(days=now.weekday() - 7)
    last_week_end = over_today - timedelta(days=now.weekday() - 13)

    return last_week_start, last_week_end


def work_duration(start_time, end_time):
    time_delta = end_time - start_time
    day_delta = time_delta.days
    sec_delta = time_delta.seconds

    if day_delta < 1:
        hours = round(sec_delta / 3600)
        if 3 <= hours <= 5:
            duration = '0.5天'
        elif hours > 5:
            duration = '1天'
        else:
            duration = f'{hours}小时'
    else:
        s = ''
        pre = ''
        hours = round(sec_delta / 3600)
        if hours >= 4:
            s = '.5'
        if hours >= 7:
            pre = '>'
        duration = f'{pre}{day_delta}{s}天'

    return duration


def today_date(sp=''):
    now = datetime.datetime.now()
    if sp == '-':
        return now.strftime('%Y-%m-%d')
    elif sp == '.':
        return now.strftime('%Y.%m.%d')
    elif sp == '/':
        return now.strftime('%Y/%m/%d')
    else:
        return now.strftime('%Y%m%d')
