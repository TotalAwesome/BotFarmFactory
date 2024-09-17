URL_INIT = "https://space.executor.tg/"
URL_VERIFY = "https://space-backend.executor.tg/api/auth/verify"  # POST {"hash": "initData"}
URL_VERIFICATION = "https://space-backend.executor.tg/api/auth/verification"  # POST {"hash": "initData"}
URL_CLAIMED = "https://space-backend.executor.tg/api/user-claim-history/claimed"
URL_CLAIM = "https://space-backend.executor.tg/api/user-claim-history/create"
URL_TASKS = "https://space-backend.executor.tg/api/tasks/all"  # GET
URL_BEGIN_TASK = "https://space-backend.executor.tg/api/tasks-history/create"  # POST {"uuid": ""}
URL_CLAIM_TASK = "https://space-backend.executor.tg/api/tasks-history/claimed"  # POST {"uuid": ""}
URL_CLAIM_DAILY_REWARD = "https://space-backend.executor.tg/api/user-login-history/claim"
URL_START_GAME = ""

MSG_CLAIM = "Собрал нафармленное и начал фармить"
MSG_STATE = "Баланс: {balance}"

HEADERS = {
    "sec-ch-ua": 'Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122',
    "sec-ch-ua-mobile": "?1" ,
    "sec-ch-ua-platform": "Android",
    "upgrade-insecure-requests": "1" ,
    "user-agent": "Mozilla/5.0 (Linux; Android 11; Redmi 5 Plus Build/RQ3A.210805.001.A1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/122.0.6261.64 Mobile Safari/537.36" ,
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7" ,
    "x-requested-with": "org.telegram.messenger" ,
    "sec-fetch-site": "none" ,
    "sec-fetch-mode": "navigate" ,
    "sec-fetch-user": "?1" ,
    "sec-fetch-dest": "document" ,
    "accept-language": "ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7",
    "Authorization": "Bearer",
    "Anon-Auth": None
}
