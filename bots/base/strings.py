URL_CHECK_IP = 'https://httpbin.org/ip'
MSG_PROXY_IP = "Прокси работает. Ваш IP через прокси: {ip}"
MSG_PROXY_CHECK_ERROR = "Ошибка при проверке прокси. Код ответа: {status_code}"
MSG_PROXY_CONNECTION_ERROR = "Не удалось подключиться через прокси: {error}"
MSG_BAD_RESPONSE = "Плохой ответ от сервера: {status} {text}"
MSG_SESSION_ERROR = "Ошибка во время выполнения запроса: {error}"
BASE_NAME = 'BaseFarmer'


USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 15.1; X96Q_PRO2 Build/QP1A.191105.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.149 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11.3; YD206 Build/P1NKL07U5) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/101.0.4951.54 Mobile Safari/537.36	Android 11.3",
    "Mozilla/5.0 (Linux; Android 12.1; SM-G998U Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/64.0.3282.116 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12.1; SM-G996W Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/64.0.3282.116 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12.0.1; zh-cn; Pixel 6 Pro; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/98.0.4758.46 Mobile Safari/537.36 SearchCraft/3.7.0 (Baidu; P1 9)",
    "Mozilla/5.0 (Linux; Android 11; Android SDK built for x86_64 Build/RSR1.210722.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 4a Build/TQ3A.230805.001.S1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.179 Mobile Safari/537.36 App Version:4.0.9.3",
    "Mozilla/5.0 (Linux; Android 13; CPH2251 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.26 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-A715W Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; V2322; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36 VivoBrowser/12.3.2.3",
]

LOG_TEMPLATE = "[ {user} | {ip} | {farmer_name} ] >> {message}"