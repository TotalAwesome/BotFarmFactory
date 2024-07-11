API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impqdm5tb3luY21jZXdudXlreWlkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDg3MDE5ODIsImV4cCI6MjAyNDI3Nzk4Mn0.oZh_ECA6fA2NlwoUamf1TqF45lrMC0uIdJXvVitDbZ8'

URL_INIT = "https://dot.dapplab.xyz/"
URL_GET_TOKEN = "https://jjvnmoyncmcewnuykyid.supabase.co/functions/v1/getToken"
URL_GET_USER_INFO = "https://jjvnmoyncmcewnuykyid.supabase.co/rest/v1/rpc/get_user_info"
URL_SAVE_COINS = "https://jjvnmoyncmcewnuykyid.supabase.co/rest/v1/rpc/save_coins"
URL_TRY_YOUR_LUCK = "https://jjvnmoyncmcewnuykyid.supabase.co/rest/v1/rpc/try_your_luck"
URL_ADD_MULTITAP = "https://jjvnmoyncmcewnuykyid.supabase.co/rest/v1/rpc/add_multitap"
URL_ADD_ATTEMPT = "https://jjvnmoyncmcewnuykyid.supabase.co/rest/v1/rpc/add_attempts"

MSG_AUTH = "Получение токена"
MSG_INIT_SUCCESS = "Инициализация успешна!"
MSG_INIT_ERROR = "Ошибка инициализации!"
MSG_BALANCE = "Баланс: {balance}"
MSG_LEVEL = "Уровень: {level}"
MSG_ENERGY = "Энергия: {energy}"
MSG_LIMIT_ENERGY = "Лимит энергии: {limit_energy}"
MSG_MULTITAP_LEVEL = "Мультитап: {multitap_level}"
MSG_GAME_PLAYED = "Игра сыграна! +{coins:,}"
MSG_GAME_NOT_PLAYED = "Игра не сыграна!"
MSG_BONUS_RECEIVED = "Бонус получен! +150,000"
MSG_BONUS_ALREADY_RECEIVED = "Бонус не активен!"
MSG_BONUS_NOT_RECEIVED = "Бонус не получен!"
MSG_BOOST_SUCCESS = "{boost_name}: успешно улучшен!"
MSG_BOOST_ALREADY_MAX = "{boost_name}: уже на максимальном уровне"
MSG_BOOST_FAILED = "{boost_name}: не удалось улучшить"

BOOST_NAMES = {
    "Click_LVL": "Мультитап",
    "Limit_LVL": "Лимит энергии"
}

HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/json",
    "cache-control": "no-cache",
    "origin": "https://dot.dapplab.xyz",
    "referer": "https://dot.dapplab.xyz/",
    "sec-ch-ua": 'Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122',
    "x-requested-with": "org.telegram.plus",
    "x-client-info": "postgrest-js/1.9.2",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "Android",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
