URL_GET_MINING_BLOCKS = "https://api.simple.app/api/v1/public/telegram/get-mining-blocks/" # POST
URL_GET_TASK_LIST = "https://api.simple.app/api/v1/public/telegram/get-task-list-2/" # POST
URL_START_TASK = "https://api.simple.app/api/v1/public/telegram/start-task-start-2/" # POST {userid, auth_data, type, id}
URL_CHECK_TASK = "https://api.simple.app/api/v1/public/telegram/check-task-check-2/" # POST {userid, auth_data, type, id}
URL_BUY_UPGRADE = "https://api.simple.app/api/v1/public/telegram/buy-mining-block/" # POST {level, mineid}
URL_CLAIM_FRIENDS = "https://api.simple.app/api/v1/public/telegram/claim_friends/" # POST 
URL_CLAIM_SPIN = "https://api.simple.app/api/v1/public/telegram/claim-spin/" # POST {userId, authData, frontCoef, amount}
URL_START_FARM = "https://api.simple.app/api/v1/public/telegram/activate/"  # POST
URL_CLAIM_FARMED = "https://api.simple.app/api/v1/public/telegram/claim/" # POST
URL_FRIENDS = "https://api.simple.app/api/v1/public/telegram/friends/" # POST
URL_SPIN = "https://api.simple.app/api/v1/public/telegram/claim-spin/"
URL_PROFILE = "https://api.simple.app/api/v1/public/telegram/profile/" # POST
URL_TAP = "https://api.simple.app/api/v1/public/telegram/tap/" # POST {userid, authdata, count}
URL_INIT = "https://simpletap.app/version_05/"


MSG_PROFILE_UPDATE = "Обновление профиля"
MSG_TAP = "Натапал {taps} монет"
MSG_START_FARMING = "Начал фармить"
MSG_START_TASK = "Запустил таску"
MSG_BUY_UPGRADE = "Прокачал: {name} ({level}) цена: {price} окупаемость: {payback}"
MSG_SPIN = "Крутанул рулетку, получил: {type} кол-во: {amount}"
MSG_CLAIM_FARM = "Собрал нафармленное: {amount}"
MSG_CLAIM_REFS = "Собрал нафармленное рефами: {amount}"
MSG_STATE = "Баланс: {balance} | Прибыль в час: {mine_per_hour} | тапов в час: {taps_per_hour}"

class UpgradeTypes:
    TAPS_LIMIT = 1
    PASSIVE_EARN = 2
    TAP_SIZE = 3

SPIN_TYPES = {
    0: "лимит тапов",
    1: "добыча",
    2: "размер тапа",
    3: "монеты",
}

HEADERS = {
    'Host' : 'api.simple.app',
    'sec-ch-ua' : '"Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122"',
    'accept' : 'application/json, text/plain, */*',
    'content-type' : 'application/json',
    'sec-ch-ua-mobile' : '?1',
    'user-agent' : 'Mozilla/5.0 (Linux; Android 11; Samsung Galaxy S22; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/122.0.6261.64 Mobile Safari/537.36',
    'sec-ch-ua-platform' : 'Android',
    'origin' : 'https://simpletap.app',
    'x-requested-with' : 'org.telegram.messenger',
    'sec-fetch-site' : 'cross-site',
    'sec-fetch-mode' : 'cors',
    'sec-fetch-dest' : 'empty',
    'referer' : 'https://simpletap.app/',
    'accept-language' : 'ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7',
    }
