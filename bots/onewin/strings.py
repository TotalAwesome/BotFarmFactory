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
MSG_BUY_BUILDING = "Здание {name} куплено"

BUILDING_INFO = {
    "coinflip": {"purchase_id": "coinflip1", "rus_name": "Такси",
                 "requirements": None,
                 "min_balance": 2_000},
    "mines": {"purchase_id": "Mines1", "rus_name": "Продуктовый магазин",
              "requirements": None,
              "min_balance": 2_000},
    "bombucks": {"purchase_id":"Bombucks1", "rus_name": "Стриминг",
                 "requirements": None,
                 "min_balance": 2_000},
    "tower": {"purchase_id":"Tower1", "rus_name": "Майнинг ферма",
              "requirements": None,
              "min_balance": 2_000},
    "double":{"purchase_id":"Double1", "rus_name": "Барбершоп",
              "requirements": {"name":"mines", "level":8},
              "min_balance": 10_000},
    "royalmines":{"purchase_id":"RoyalMines1", "rus_name": "Автосалон",
                  "requirements": {"name":"coinflip", "level":5},
                  "min_balance": 10_000},
    "luckyloot":{"purchase_id":"LuckyLoot1", "rus_name": "Рекламное агентство",
                 "requirements": {"name":"coinflip", "level":11},
                 "min_balance": 10_000},
    "brawlpirates":{"purchase_id":"BrawlPirates1", "rus_name": "Компьютерный клуб",
                    "requirements": {"name":"bombucks", "level":3},
                    "min_balance": 10_000},
    "anubisplinko":{"purchase_id":"AnubisPlinko1", "rus_name": "Фитнес клуб",
                    "requirements": {"name":"tower", "level":7},
                    "min_balance": 20_000},
    "rocketx":{"purchase_id":"RocketX1", "rus_name": "Кинотеатр",
               "requirements": {"name":"anubisplinko", "level":10},
               "min_balance": 20_000},
    "speedncash":{"purchase_id":"SpeednCash1", "rus_name": "Торговый центр",
                  "requirements": {"name":"rocketx", "level":9},
                  "min_balance": 20_000},
    "rocketqueen":{"purchase_id":"RocketQueen1", "rus_name": "Отель",
                   "requirements": {"name":"speedncash", "level":12},
                   "min_balance": 20_000},
    "luckyjet":{"purchase_id":"LuckyJet1", "rus_name": "Маркетплейс",
                   "requirements": {"name":"brawlpirates", "level":7},
                   "min_balance": 20_000},
    "airjet":{"purchase_id":"AirJet1", "rus_name": "Каршеринг",
                   "requirements": {"name":"anubisplinko", "level":7},
                   "min_balance": 20_000},
    "fortunecrash":{"purchase_id":"FortuneCrash1", "rus_name": "Онлайн школа",
                   "requirements": {"name":"luckyloot", "level":3},
                   "min_balance": 20_000}
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

