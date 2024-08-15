URL_INIT = "https://crypto-clicker-backend-go-prod.100hp.app/game/start"
URL_ACCOUNT_BALANCE = "https://crypto-clicker-backend-go-prod.100hp.app/user/balance" #GET
URL_DAILY_REWARD_INFO = "https://crypto-clicker-backend-go-prod.100hp.app/tasks/everydayreward" #GET
URL_TAP = "https://crypto-clicker-backend-go-prod.100hp.app/tap" #POST
URL_MINING = "https://crypto-clicker-backend-go-prod.100hp.app/minings" #GET
URL_MINING_UPGRADE = "https://crypto-clicker-backend-go-prod.100hp.app/minings" #POST Пример id: "coinflip15"
URL_FRIENDS_INFO = "https://crypto-clicker-backend-go-prod.100hp.app/friends?offset=0&limit=5"
URL_FRIEND_CLAIM = "https://crypto-clicker-backend-go-prod.100hp.app/friends/collect" #POST

MSG_INITIALIZATION_ERROR = "Ошибка инициализации"
MSG_ACCESS_TOKEN_ERROR = "Не удалось получить access token"
MSG_AUTHENTICATION_ERROR = "Ошибка аутентификации. Код состояния: {status_code}, Ответ: {text}"
MSG_URL_ERROR = "Ошибка при разборе URL для аутентификации: {error}"
MSG_ACCOUNT_INFO_ERROR = "Не получена информация об аккаунте. Код состояния: {status_code}, Ответ: {text}"
MSG_CURRENT_BALANCE = "Текущий баланс - {coins} монет"
MSG_BUY_UPGRADE = "Прокачал: {name} : ур.{level}"
MSG_DAILY_REWARD = "Забрал ежедневную награду - {coins} монет"
MSG_DAILY_REWARD_STATE_ERROR = "Не получена информация об ежедневной награде. Код состояния: {status_code}, Ответ: {text}"
MSG_DAILY_REWARD_CLAIM_ERROR = "Не получена ежедневная награда. Код состояния: {status_code}, Ответ: {text}"
MSG_DAILY_REWARD_IS_COLLECTED = "Ежедневная награда уже получена"
MSG_FRIENDS_REWARD = "Забрал награду от рефералов - {coins} монет"
MSG_FRIENDS_REWARD_ERROR = "Не получена награда от рефералов. Код состояния: {status_code}, Ответ: {text}"
MSG_BUY_BUILDING = "Здание {name} куплено"

BUILDING_INFO = {
    "coinflip": {"purchase_id": "coinflip1", "rus_name": "Такси",
                 "requirements": None,
                 "min_balance": 150},
    "mines": {"purchase_id": "Mines1", "rus_name": "Продуктовый магазин",
              "requirements": None,
              "min_balance": 340},
    "bombucks": {"purchase_id":"Bombucks1", "rus_name": "Стриминг",
                 "requirements": None,
                 "min_balance": 480},
    "tower": {"purchase_id":"Tower1", "rus_name": "Майнинг ферма",
              "requirements": None,
              "min_balance": 555},
    "double":{"purchase_id":"Double1", "rus_name": "Барбершоп",
              "requirements": {"name":"mines", "level":8},
              "min_balance": 10_000},
    "royalmines":{"purchase_id":"RoyalMines1", "rus_name": "Автосалон",
                  "requirements": {"name":"coinflip", "level":5},
                  "min_balance": 1_500},
    "luckyloot":{"purchase_id":"LuckyLoot1", "rus_name": "Рекламное агентство",
                 "requirements": {"name":"coinflip", "level":11},
                 "min_balance": 2_200},
    "brawlpirates":{"purchase_id":"BrawlPirates1", "rus_name": "Компьютерный клуб",
                    "requirements": {"name":"bombucks", "level":3},
                    "min_balance": 4_000},
    "anubisplinko":{"purchase_id":"AnubisPlinko1", "rus_name": "Фитнес клуб",
                    "requirements": {"name":"tower", "level":7},
                    "min_balance": 5_500},
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
                   "min_balance": 50_000},
    "metacrash":{"purchase_id":"MetaCrash1", "rus_name": "Сервис доставки",
                 "requirements": {"name":"fortunecrash", "level":7},
                 "min_balance": 50_000},
    "starx":{"purchase_id":"StarX", "rus_name": "IT-компания",
             "requirements": {"name":"rocketqueen", "level":5},
             "min_balance": 100_000},
    "semiconductor":{"purchase_id":"semiconductor1", "rus_name": "Социальная сеть", #$cryptocliker_semiconductor_manufacturing
                     "requirements": {"name":"starx", "level":5},
                     "min_balance": 100_000},
    "renewenergy":{"purchase_id":"renewenergy1", "rus_name": "Банк",
                   "requirements": {"name":"starx", "level":10},
                   "min_balance": 150_000},
    # "":{"purchase_id":"", "rus_name": "Крипто биржа",
    #                "requirements": {"name":"", "level":20},
    #                "min_balance": 200_000},
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

