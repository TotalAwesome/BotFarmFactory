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
URL_BUY_SKIN = "https://api.hamsterkombatgame.io/clicker/buy-skin" #POST

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