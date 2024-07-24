URL_INIT = 'https://onetime.dog/'
URL_LOGIN = 'https://api.onetime.dog/join'
URL_FRIENDS = 'https://api.onetime.dog/frens'

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9',
    'Dnt': '1',
    'Referer': 'https://onetime.dog/',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Sec-Gpc': '1',
    'Sec-Ch-Ua-Mobile': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
}

MSG_CURRENT_BALANCE = "Текущий баланс: {balance}"
MSG_CURRENT_FRIENDS = "Рефералов: {total}"
MSG_LOGIN_ERROR = "Ошибка при логине: {e}"
