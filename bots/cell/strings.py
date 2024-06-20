URL_INIT = "https://cell-frontend.s3.us-east-1.amazonaws.com/telegram-mini-app/index.html"
URL_PROFILE = "https://cellcoin.org/init" # POST
URL_TAP = "https://cellcoin.org/clicks" # POST {userid, authdata, count}
URL_CLAIM = "https://cellcoin.org/claim"

MSG_PROFILE_UPDATE = "Обновление профиля"
MSG_TAP = "Натапал {taps} монет"
MSG_CLAIM = "Собрал нафармленное: {amount}"
MSG_STATE = "Баланс: {balance}"

HEADERS = {
    'sec-ch-ua': 'Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122',
    'sec-ch-ua-mobile': '?1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; Redmi 5 Plus Build/RQ3A.210805.001.A1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/122.0.6261.64 Mobile Safari/537.36',
    'sec-ch-ua-platform': 'Android',
    'Accept': '*/*',
    'Origin': 'https://cell-frontend.s3.us-east-1.amazonaws.com',
    'X-Requested-With':	'org.telegram.messenger',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    }
