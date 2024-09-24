# взаимодействие с API игры
URL_CLAIM_DAILY_CIPHER = "https://api.hamsterkombatgame.io/clicker/claim-daily-cipher"
URL_CLAIM_DAILY_COMBO = "https://api.hamsterkombatgame.io/clicker/claim-daily-combo"
URL_UPGRADES_FOR_BUY = "https://api.hamsterkombatgame.io/clicker/upgrades-for-buy"
URL_SELECT_EXCHANGE ="https://api.hamsterkombatgame.io/clicker/select-exchange"
URL_BOOSTS_FOR_BUY = "https://api.hamsterkombatgame.io/clicker/boosts-for-buy"
URL_AUTH = "https://api.hamsterkombatgame.io/auth/auth-by-telegram-webapp"
URL_BUY_UPGRADE = "https://api.hamsterkombatgame.io/clicker/buy-upgrade"
URL_LIST_TASKS = "https://api.hamsterkombatgame.io/clicker/list-tasks"
URL_CHECK_TASK = "https://api.hamsterkombatgame.io/clicker/check-task"
URL_BUY_BOOST = "https://api.hamsterkombatgame.io/clicker/buy-boost"
URL_CONFIG = "https://api.hamsterkombatgame.io/clicker/config"
URL_SYNC = "https://api.hamsterkombatgame.io/clicker/sync"
URL_TAP = "https://api.hamsterkombatgame.io/clicker/tap"
URL_INIT = "https://api.hamsterkombatgame.io/clicker"
URL_GET_SKINS = "https://api.hamsterkombatgame.io/clicker/get-skin"
URL_BUY_SKIN = "https://api.hamsterkombatgame.io/clicker/buy-skin" #POST\
URL_GET_PROMOS = "https://api.hamsterkombatgame.io/clicker/get-promos"
URL_APPLY_PROMO = "https://api.hamsterkombatgame.io/clicker/apply-promo"

# взаимодействие с генератором промокодов
URL_REGISTER_EVENT = "https://api.gamepromo.io/promo/register-event"
URL_LOGIN = "https://api.gamepromo.io/promo/login-client"
URL_CREATE_CODE = "https://api.gamepromo.io/promo/create-code"

# шаблоны сообщений в лог
MSG_BUY_UPGRADE = "Прокачал: {name} : ур.{level} за {price} даст +{profitPerHourDelta}/час"
MSG_SESSION_ERROR = "Ошибка во время выполнения запроса: {error}"
MSG_COMBO_EARNED = "Получено вознаграждение за комбо: {coins}"
MSG_BAD_RESPONSE = "Плохой ответ от сервера: {status} {text}"
MSG_CLAIMED_COMBO_CARDS = "Уже получены комбо карты: {cards}"
MSG_CRYPTED_CIPHER = "Шифрованный шифр: {cipher}"
MSG_TAP = "Тапнул на {taps_count} монеток"
MSG_CIPHER = "Новый шифр: {cipher}"
MSG_SYNC = "Обновление данных"
MSG_TASK_COMPLETED = "Задание выполнено. Награда: {reward}"
MSG_TASK_NOT_COMPLETED = "Задание не выполнено"
MSG_BUY_SKIN = "Скин {skin_name} куплен"


MSG_PROMO_UPDATE_ERROR = "Ошибка обновления статуса промкодов"
MSG_PROMO_STATUS = "Осталось ввести промокодов: {keys_left_status}"
MSG_PROMO_COMPLETED = "Все промокоды введены"
MSG_PROMO_OK = "Промокод применен успешно"
MSG_PROMO_ERROR = "Промокод не применен"
MSG_TRY_PROMO = "Попытка применения промокода: {code}"


BOOST_ENERGY = "BoostFullAvailableTaps"

HEADERS = {
    "Connection":	"keep-alive",
    "sec-ch-ua":	'"Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122"',
    "sec-ch-ua-mobile":	'?1',
    "user-agent":	"Mozilla/5.0 (Linux; Android 11; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/122.0.6261.64 Mobile Safari/537.36",
    "sec-ch-ua-platform":	'"Android"',
    "Accept":	"*/*",
    "Origin":	"https://hamsterkombatgame.io",
    "X-Requested-With":	"org.telegram.messenger",
    "Sec-Fetch-Site":	"same-site",
    "Sec-Fetch-Mode":	"cors",
    "Sec-Fetch-Dest":	"empty",
    "Referer":	"https://hamsterkombatgame.io/",
    "Accept-Encoding":	"gzip, deflate, br",
}

GET_PROMO_HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                     "Content-Type": "application/json; charset=utf-8",
                     "Host": "api.gamepromo.io"}

PROMO_TOKENS = {
    # promo_id : app_token
    'b4170868-cef0-424f-8eb9-be0622e8e8e3': 'd1690a07-3780-4068-810f-9b5bbf2931b2', # CUBE
    'c4480ac7-e178-4973-8061-9ed5b2e17954': '82647f43-3f87-402d-88dd-09a90025313f', # TRAIN
    'dc128d28-c45b-411c-98ff-ac7726fbaea4': '8d1cc2ad-e097-4b86-90ef-7a27e19fb833', # MERGE
    '61308365-9d16-4040-8bb0-2f4a4c69074c': '61308365-9d16-4040-8bb0-2f4a4c69074c', # TWERK
    '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71': '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71', # POLY
    'ef319a80-949a-492e-8ee0-424fb5fc20a6': 'ef319a80-949a-492e-8ee0-424fb5fc20a6', # TRIM
    'b2436c89-e0aa-4aed-8046-9b0515e1c46b': 'b2436c89-e0aa-4aed-8046-9b0515e1c46b', # ZooPolis
    '112887b0-a8af-4eb2-ac63-d82df78283d9': '112887b0-a8af-4eb2-ac63-d82df78283d9', # Fluff Crusade
    'e68b39d2-4880-4a31-b3aa-0393e7df10c7': 'e68b39d2-4880-4a31-b3aa-0393e7df10c7', # Tile Trio
    '04ebd6de-69b7-43d1-9c4b-04a6ca3305af': '04ebd6de-69b7-43d1-9c4b-04a6ca3305af', # Stone Age
}
