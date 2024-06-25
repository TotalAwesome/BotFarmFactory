TELEGRAM_ACCOUNTS = [
    dict(phone='+99999999999', proxy="http://user:pass@host:port"),
    dict(phone='+99999999991', proxy="https://user:pass@host:port"),
    dict(phone='+55555555544'),
]

try:
    from accounts_local import *
except ImportError:
    pass
