import random
import string
from datetime import datetime
from itertools import cycle

from core.pos.choices import EMISSION_TYPE


def get_modulo_11_algorithm(pass_key_48=''):
    if len(pass_key_48) > 48:
        return ''
    addition = 0
    factors = cycle((2, 3, 4, 5, 6, 7))
    for digit, factor in zip(reversed(pass_key_48), factors):
        addition += int(digit) * factor
    control = 11 - addition % 11
    if control == 11:
        control = 0
    elif control == 10:
        control = 1
    return str(control)


def get_numeric_code(amount=8):
    numbers = list(string.digits)
    return ''.join(random.choices(numbers, k=amount))


def generate_access_key(instance):
    formatted_date = f"{datetime.now().strftime('%d%m%Y')}"
    pass_key_48 = f'{formatted_date}{instance.receipts.code}{instance.company.ruc}{instance.company.environment_type}{instance.company.establishment_code}{instance.company.issuing_point_code}{instance.voucher_number}{get_numeric_code()}{EMISSION_TYPE[0][0]}'
    module11 = get_modulo_11_algorithm(pass_key_48=pass_key_48)
    if len(module11):
        return f'{pass_key_48}{module11}'
    return None
