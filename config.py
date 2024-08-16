ACCOUNTS_DIR = "accounts_data"
# TELEGRAM WEB
TELEGRAM_AUTH = dict(
    api_id=2496,
    api_hash="8da85b0d5bfe62527e5b244c209159c3",
    device_model="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    system_version="Windows",
    app_version="1.57 Z",
    lang_code="en",
    system_lang_code="en-US",
)

DEBUG = True
RETRY_ATTEMPTS = 3

ENABLED_BOTS = [
    # Пустой список = все боты включены
    # иначе будут работать только те, что в этом списке
]

SLEEP_AT_NIGHT = False  # При True ночью фарминг не производится
NIGHT_HOURS = (0, 7)  # Диапазон времени, когда у фермы тихий час
MULTITHREAD = False  # При True на каждый аккаунт будет отдельный поток

try:
    from config_local import *
except ImportError:
    pass
