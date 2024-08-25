import re


def is_valid_phone_number(phone_number):
    # Регулярное выражение для проверки номера телефона в формате +7XXXXXXXXXX
    pattern = r'^\+7\d{10}$'

    # Используем re.match для проверки соответствия регулярному выражению
    if re.match(pattern, phone_number):
        return True
    else:
        return False
