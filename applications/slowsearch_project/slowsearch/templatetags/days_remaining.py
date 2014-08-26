__author__ = 'Craig'

from django import template
import datetime

register = template.Library()


def get_remaining_day():
    date = datetime.datetime.strptime('22082014', '%d%m%Y')
    current_date = date.today().day
    days_remaining = date.day - current_date
    return days_remaining

register.assignment_tag(get_remaining_day)