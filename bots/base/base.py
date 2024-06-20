import logging
from requests import Session, get as requests_get
from time import time, sleep
from datetime import datetime
from random import choice
from .strings import URL_CHECK_IP, MSG_BAD_RESPONSE, MSG_PROXY_CHECK_ERROR, MSG_PROXY_CONNECTION_ERROR, \
    MSG_PROXY_IP, MSG_SESSION_ERROR, USER_AGENTS, LOG_TEMPLATE


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def timestamp():
    return int(time())


def check_proxy(proxies):
    try:
        response = requests_get(URL_CHECK_IP, proxies=proxies)
        if response.status_code == 200:
            logging.info(MSG_PROXY_IP.format(ip=response.json()['origin']))
            return response.text
        else:
            logging.error(MSG_PROXY_CHECK_ERROR.format(status_code=response.status_code))
    except Exception as error:
        logging.error(MSG_PROXY_CONNECTION_ERROR.format(error=error))


def retry(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        while True:
            try:
                result = func(*args, **kwargs)
                if result.status_code not in (200, 201, 202):
                    if result.status_code == 429:
                        self.log(MSG_BAD_RESPONSE.format(status=result.status_code, text=result.text))
                        sleep(10)
                        continue
                    elif result.status_code in (401, 403):
                        if result.status_code == 401 and self.refreshable_token:
                            self.refresh_token()
                        self.log(MSG_BAD_RESPONSE.format(status=result.status_code, text=result.text))
                        raise Exception(f"code: {result.status_code} {result.text}")
                return result
            except Exception as error:
                self.log(MSG_SESSION_ERROR.format(error=error))
                sleep(3)
    return wrapper


class BaseFarmer(Session):

    """
    Базовый класс 
    У дочерних классов реализовать методы:
        set_headers -> Установка заголовков
        authenticate -> Аутентификация и рефреш если надо
        is_ready_to_farm -> Пора ли запускать фарминг
        farm -> Выполнение всех необходимых действий с аккаунтом за один прогон
        set_start_time -> Таймштамп следующего прогона
        refresh_token -> Если нужен рефреш
    """

    name = None # bot_username
    initiator = None
    initialization_data = {}
    account_name = None
    start_time = time()
    refreshable_token = False
    extra_code = None
    app_extra = None
    ip = None

    def __init__(self, initiator, proxy=None, only_proxy=False, **kwargs) -> None:
        super().__init__()
        self.features = kwargs
        self.set_headers()
        self.update_user_agent()
        self.initiator = initiator
        self.get_account_name()
        if proxy:
            proxies = dict(http=f"http://{proxy}", https=f"https://{proxy}")
            if check_proxy(proxies):
                self.proxies = proxies
            elif only_proxy:
                raise Exception(MSG_PROXY_CONNECTION_ERROR.format(str(kwargs)))
        if self.extra_code:
            self.initiator.prepare_bot(self.name, self.name, self.extra_code)
        self.authenticate()

    def log(self, message):
        ip = self.ip if self.ip else "no_proxy"
        logging.info(LOG_TEMPLATE.format(farmer_name=self.name.lower(), 
                                         user=self.account_name, 
                                         message=message,
                                         ip=ip))

    @retry
    def request(self, *args, **kwargs):
        return super().request(*args, **kwargs)
    
    def get_account_name(self):
        me = self.initiator.get_me()
        self.account_name = me.username or me.first_name or me.phone

    @property
    def is_ready_to_farm(self):
        return self.start_time <= time()
    
    def set_start_time(self):
        self.start_time = time() + 10 * 60

    def set_headers(self, *args, **kwargs):
        self.update_user_agent()
    
    def update_user_agent(self):
        self.headers['user-agent'] = choice(USER_AGENTS)

    def authenticate(self, *args, **kwargs):
        raise NotImplementedError
    
    def refresh_token(self, *args, **kwargs):
        raise NotImplementedError

    def farm(self):
        raise NotImplementedError

    def proceed_farming(self):
        if self.is_ready_to_farm:
            print('=' * 150)
            self.farm()
            self.set_start_time()
            self.log('Следующий заход в : {}'.format(
                datetime.fromtimestamp(self.start_time).strftime('%d-%m-%Y %H:%M:%S')
            ))
