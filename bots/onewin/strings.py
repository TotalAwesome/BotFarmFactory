URL_INIT = "https://crypto-clicker-backend-go-prod.100hp.app/game/start"

URL_ACCOUNT_BALANCE = "https://crypto-clicker-backend-go-prod.100hp.app/user/balance" #GET
URL_DAILY_REWARD_INFO = "https://crypto-clicker-backend-go-prod.100hp.app/tasks/everydayreward" #GET
URL_TAP = "https://crypto-clicker-backend-go-prod.100hp.app/tap" #POST
URL_MINING = "https://crypto-clicker-backend-go-prod.100hp.app/minings" #GET

# Прокинуть ID id "coinflip15"
URL_MINING_UPGRADE = "https://crypto-clicker-backend-go-prod.100hp.app/minings" #POST


MSG_CURRENT_BALANCE = "Текущий баланс - {coins} монет"
MSG_BUY_UPGRADE = "Прокачал: {name} : ур.{level}"
MSG_DAILY_REWARD = "Забрал ежедневную награду - {coins} монет"
MSG_DAILY_REWARD_IS_COLLECTED = "Ежедневная награда уже получена"
MSG_BUY_BUILDING = "Здание куплено"

BUILDING_INFO = {
    "coinflip": {"purchase_id": "coinflip1", "requirements": None, "min_balance": 2_000},
    "mines": {"purchase_id": "Mines1", "requirements": None, "min_balance": 2_000},
    "bombucks": {"purchase_id":"Bombucks1", "requirements": None, "min_balance": 2_000},
    "tower": {"purchase_id":"Tower1", "requirements": None, "min_balance": 2_000},
    "double":{"purchase_id":"Double1", "requirements": {"name":"mines", "level":8}, "min_balance": 10_000},
    "royalmines":{"purchase_id":"RoyalMines1", "requirements": {"name":"coinflip", "level":5}, "min_balance": 10_000},
    "luckyloot":{"purchase_id":"LuckyLoot1", "requirements": {"name":"coinflip", "level":11}, "min_balance": 10_000},
    "brawlpirates":{"purchase_id":"BrawlPirates1", "requirements": {"name":"bombucks", "level":3}, "min_balance": 10_000}
}

RUS_NAMES = {
    "coinflip": "Такси",
    "mines": "Продуктовый магазин",
    "bombucks": "Стриминг",
    "tower": "Майнинг ферма",
    "double": "Барбершоп",
    "royalmines": "Автосалон",
    "luckyloot": "Рекламное агентство",
    "brawlpirates": "Компьютерный клуб",
    "anubisplinko": "Фитнес-клуб",
    "rocketx": "Кинотеатр",
    "speedncash": "Торговый центр",
    "luckyjet": "Маркетплейс",
    "airjet": "Каршеринг",
    "fortunecrash": "Онлайн школа",
}

HEADERS = {
    'Content-Type': 'application/json',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'origin': 'https://cryptocklicker-frontend-rnd-prod.100hp.app',
    'x-requested-with': 'org.telegram.messenger',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://cryptocklicker-frontend-rnd-prod.100hp.app/',
    'accept-language': 'ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7'
}

