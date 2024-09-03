URL_INIT = 'https://xapi.tapcoins.app/system/init'
URL_LOGIN = 'https://xapi.tapcoins.app/auth/login'
URL_COLLECT = 'https://xapi.tapcoins.app/coin/collect'
URL_DAILY = 'https://xapi.tapcoins.app/daily/steps'
URL_DAILY_COMPLETE = 'https://xapi.tapcoins.app/daily/complete'
URL_CARDS_LIST = 'https://xapi.tapcoins.app/mine/task/list'
URL_CARDS_CATEGORIES = 'https://xapi.tapcoins.app/mine/category/list'
URL_CARDS_UPGRADE = 'https://xapi.tapcoins.app/mine/upgrade'
URL_LUCKY_BOUNTY = 'https://xapi.tapcoins.app/mine/lucky'
URL_USER_INFO = 'https://xapi.tapcoins.app/mine/mine'
URL_REFRESH = 'https://xapi.tapcoins.app/user/online/refresh'
URL_GET_TASKS = 'https://xapi.tapcoins.app/task/list'
URL_COMPLETE_TASK = 'https://xapi.tapcoins.app/task/complete'

HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9',
    'Content-Length': '53',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://game.tapcoins.app',
    'Priority': 'u=1, i',
    'Referer': 'https://game.tapcoins.app/',
    'Sec-Ch-Ua': 'Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122',
    'Sec-Ch-Ua-Mobile': '?1',
    'Sec-Ch-Ua-Platform': '"Android"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi 5 Plus Build/RQ3A.210805.001.A1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/122.0.6261.64 Mobile Safari/537.36'
}

MSG_STARTING_UPDATING_CARDS = 'Начало прокачивания карточек'
MSG_UPGRADING_CARDS = 'Прокачивание карточек'
MSG_UPGRADE_COMPLETE = 'Прокачка карточек завершена'
MSG_NO_CARDS_TO_UPGRADE = "Не найдены карты для прокачки"
MSG_CARD_UPGRADED = "Прокачана карта {name} до уровня {level} за {cost} монет"
MSG_NOT_ENOUGH_COINS = "Не хватает монет для прокачки"
MSG_CARD_UPGRADED_COMBO = "Прокачана карта для комбо {}"
MSG_LOGIN_BONUS_COMPLETE = "Бонус за вход {step} получен"
MSG_MAX_UPGRADES_REACHED = "Достигнут лимит прокачки {limit}"
MSG_CURRENT_BALANCE = "Текущий баланс: {balance}"
MSG_HOUR_EARNINGS = "Прибыль в час: {earnings}"
MSG_TASK_COMPLETED = "Задание {name} выполнено"

CODES = {
    "How to Win Big in Web3 Gaming": "TAPCOINS",
    "TON Chain Wallet Guide": "TONCOIN",
    "TON Chain Applications": "MINIAPP",
    "Exploring Cross-Chain Bridges": "ECONOMICS",
    "The Viral Frenzy Behind Meme Coins": "GAMEFI",
    "Making Money with DeFi": "Swaps",
    "Changing the Financial Game": "POOLS",
    "Against Volatility": "FARMING",
    "DeFi TVL for Smart Investing": "Storage"
    "The Path to Returns in DeFi": "METAVERSE"

}