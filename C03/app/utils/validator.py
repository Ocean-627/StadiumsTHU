from django.core.validators import *
from django.core.exceptions import ValidationError


def SafeValidator(content):
    number, lower, upper = False, False, False
    for c in content:
        if '0' <= c <= '9':
            number = True
        if 'a' <= c <= 'z':
            lower = True
        if 'A' <= c <= 'Z':
            upper = True
    if not (number and lower and upper):
        raise ValidationError('密码应包含大小写字母和数字')


def TimeValidator(content):
    if len(content) != 5 or content[2] != ':':
        raise ValidationError('Invalid time format, requires format like 08:00')
    hour = content[:2]
    minute = content[3:]
    if not hour.isdigit() or not minute.isdigit():
        raise ValidationError('Invalid time format, requires format like 08:00')
