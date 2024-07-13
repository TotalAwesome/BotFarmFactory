URL_CLAIM_DAILY_CIPHER = "https://api.hamsterkombat.io/clicker/claim-daily-cipher"
URL_CLAIM_DAILY_COMBO = "https://api.hamsterkombat.io/clicker/claim-daily-combo"
URL_UPGRADES_FOR_BUY = "https://api.hamsterkombat.io/clicker/upgrades-for-buy"
URL_BOOSTS_FOR_BUY = "https://api.hamsterkombat.io/clicker/boosts-for-buy"
URL_AUTH = "https://api.hamsterkombat.io/auth/auth-by-telegram-webapp"
URL_BUY_UPGRADE = "https://api.hamsterkombat.io/clicker/buy-upgrade"
URL_LIST_TASKS = "https://api.hamsterkombat.io/clicker/list-tasks"
URL_CHECK_TASK = "https://api.hamsterkombat.io/clicker/check-task"
URL_BUY_BOOST = "https://api.hamsterkombat.io/clicker/buy-boost"
URL_CONFIG = "https://api.hamsterkombat.io/clicker/config"
URL_SYNC = "https://api.hamsterkombat.io/clicker/sync"
URL_TAP = "https://api.hamsterkombat.io/clicker/tap"
URL_INIT = "https://api.hamsterkombat.io/clicker"

MSG_BUY_UPGRADE = "Прокачал: {name} : ур.{level} за {price} даст +{profitPerHourDelta}/час"
MSG_SESSION_ERROR = "Ошибка во время выполнения запроса: {error}"
MSG_COMBO_EARNED = "Получено вознаграждение за комбо: {coins}"
MSG_BAD_RESPONSE = "Плохой ответ от сервера: {status} {text}"
MSG_CLAIMED_COMBO_CARDS = "Уже получены комбо карты: {cards}"
MSG_CRYPTED_CIPHER = "Шифрованный шифр: {cipher}"
MSG_TAP = "Тапнул на {taps_count} монеток"
MSG_CIPHER = "Новый шифр: {cipher}"
MSG_SYNC = "Обновление данных"
MSG_PROXY_IP = "Прокси работает. Ваш IP через прокси: {ip}"
MSG_PROXY_CHECK_ERROR = "Ошибка при проверке прокси. Код ответа: {status_code}"
MSG_PROXY_CONNECTION_ERROR = "Не удалось подключиться через прокси: {error}"

BOOST_ENERGY = "BoostFullAvailableTaps"

HEADERS = {
    "Connection":	"keep-alive",
    "sec-ch-ua":	'"Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122"',
    "sec-ch-ua-mobile":	'?1',
    "user-agent":	"Mozilla/5.0 (Linux; Android 11; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/122.0.6261.64 Mobile Safari/537.36",
    "sec-ch-ua-platform":	'"Android"',
    "Accept":	"*/*",
    "Origin":	"https://hamsterkombat.io",
    "X-Requested-With":	"org.telegram.messenger",
    "Sec-Fetch-Site":	"same-site",
    "Sec-Fetch-Mode":	"cors",
    "Sec-Fetch-Dest":	"empty",
    "Referer":	"https://hamsterkombat.io/",
    "Accept-Encoding":	"gzip, deflate, br",
}
