from datetime import date
from collections import deque
from telegram_bot.config import MAX_LEN_DEQUE


EXCEPT = {}


def deque_work(elem, _type=None, _deque=EXCEPT):
    key = str(date.today())

    if key not in _deque:
        _deque[key] = deque(maxlen=MAX_LEN_DEQUE)

    val = (elem, _type)

    if not _type:
        result = ([i for i in EXCEPT[key] if i[0] == elem] + [None])[0]
    else:
        result = elem in _deque[key]
        if not result:
            _deque[key].append(val)

    if len(_deque.keys()) != 1:
        _deque[key] = {key: _deque[key]}

    return result
