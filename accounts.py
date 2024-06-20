try:
    from accounts_local import *
except ImportError:

    TELEGRAM_ACCOUNTS = [
        dict(phone='+99999999999', proxy="user:pass@host:port"),
        dict(phone='+99999999991', proxy="user:pass@host:port"),
        dict(phone='+55555555544'),
    ]
