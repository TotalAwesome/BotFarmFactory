URL_INIT = 'https://app.altooshka.io/'
URL_LOGIN = 'https://api.altooshka.io/user/'
URL_FOLLOW = 'https://api.altooshka.io/user/follow/'
URL_GIRLS_ACTION = 'https://api.altooshka.io/girls/action/'
URL_X_CHALLENGE = 'https://api.altooshka.io/action/challenge'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9',
    'Dnt': '1',
    'Referer': 'https://app.altooshka.io/',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Sec-Gpc': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
}

MSG_CURRENT_BALANCE = "Текущий баланс: {balance}"
MSG_ACTION_COMPLETE = "Действие {action}, девушка {girl}. +{reward} монет"
MSG_ACTION_UNDRESS_COMPLETE = "Раздел девушку {girl}. {reward} монет"
MSG_ACTION_IS_NOT_AVAILABLE = "Действие {action} для девушки {girl} ещё выполняется"

MSG_GIRL_ACTIONS_AVAILABLE = "Для девушки {girl} с уровнем {level} открыто {total} действия"
MSG_GIRL_ACTIONS_UNAVAILABLE = "Для девушки {girl} с уровнем {level} нет доступных действий"
MSG_X_CHALLENGE_SUBSCRIBED = "Подписался на канал в X"
