from re import findall
from datetime import date
from collections import deque
from telegram_bot.config import MAX_LEN_DEQUE

CACHE = deque(maxlen=500)
REGISTRATION = {}


def cache(key, value=None):
    is_new = [i[1] for i in CACHE if i[0] == key] or [None]
    if not value:
        return is_new[0]

    if not is_new[0] and value:
        CACHE.append((key, value))


def deque_work(elem, command, _type=None):
    key = str(date.today())

    if key not in REGISTRATION:
        REGISTRATION[key] = deque(maxlen=MAX_LEN_DEQUE)
        if len(REGISTRATION.keys()) != 1:
            REGISTRATION[key] = {key: REGISTRATION[key]}

    result = None
    if command == 'r':
        result = ([(i, v) for i, v in enumerate(REGISTRATION[key]) if v[0] == elem] + [None, ])[0]
        if result:
            REGISTRATION[key][result[0]] = (None, None)
            result = result[1]
    elif command == 'w':
        result = elem in REGISTRATION[key]
        if not result:
            REGISTRATION[key].append((elem, _type))

    return result


def format_data(formaring, *args):

    if not args or any([len(i) != len(args[0]) for i in args]) or not formaring:
        return ''

    result = []
    for row in args:
        list_data = [i for i, j in enumerate(row) if isinstance(j, list)]
        if list_data:
            row = list(row)
        for l in list_data:
            row[l] = f'[{", ".join(str(i) for i in row[l] if i)}]'

        if findall(r'{[\d]+}', formaring):
            string = formaring.format(*row)
        else:
            string = formaring.format(**row)

        result.append(string)

    return '\n'.join(result)


def format_group(group):
    return str(group or '').lower().replace(' ', '').replace('-', '').replace('_', '')


class MyException(Exception):
    pass

