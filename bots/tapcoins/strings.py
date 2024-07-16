URL_INIT = 'https://api.tapcoins.app/system/init'
URL_LOGIN = 'https://api.tapcoins.app/auth/login'
URL_COLLECT = 'https://api.tapcoins.app/coin/collect'
URL_DAILY = 'https://api.tapcoins.app/daily/steps'
URL_DAILY_COMPLETE = 'https://api.tapcoins.app/daily/complete'
URL_CARDS_LIST = 'https://api.tapcoins.app/mine/task/list'
URL_CARDS_CATEGORIES = 'https://api.tapcoins.app/mine/category/list'
URL_CARDS_UPGRADE = 'https://api.tapcoins.app/mine/upgrade'
URL_LUCKY_BOUNTY = 'https://api.tapcoins.app/mine/lucky'

HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9',
    'Content-Length': '53',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://game.tapcoins.app',
    'Priority': 'u=1, i',
    'Referer': 'https://game.tapcoins.app/',
    'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
}

MSG_CURRENT_BALANCE = 'Текущий баланс: {result}'
MSG_STARTING_UPDATING_CARDS = 'Начало прокачивания карточек'
MSG_UPDATING_CARDS = 'Прокачивание карточек'
MSG_UPGRADE_COMPLETE = 'Прокачка карточек завершена'
MSG_NO_CARDS_TO_UPGRADE = "Не найдены карты для прокачки"
MSG_SORTING_CARDS = "Сортирую карточки по уровню дохода"
MSG_CARD_UPGRADED = "Прокачана карта {}"
MSG_NOT_ENOUGH_COINS = "Не хватает монет для прокачки"
MSG_CARD_UPGRADED_COMBO = "Прокачана карта для комбо {}"
MSG_LOGIN_BONUS_COMPLETE = "Бонус за вход {step} получен"
