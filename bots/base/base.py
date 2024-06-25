
from time import time
from datetime import datetime
from random import choice
from requests import Session
from .utils import check_proxy, retry, logging
from .strings import USER_AGENTS, LOG_TEMPLATE, MSG_PROXY_CONNECTION_ERROR


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
            proxies = dict(http=proxy, https=proxy)
            if ip := check_proxy(proxies):
                self.ip = ip
                self.proxies = proxies
            elif only_proxy:
                raise Exception(MSG_PROXY_CONNECTION_ERROR.format(str(kwargs)))
        if self.extra_code:
            self.initiator.prepare_bot(self.name, self.name, self.extra_code)
        self.authenticate()

    def log(self, message, error=False):
        ip = self.ip if self.ip else "no_proxy"
        log_method = logging.error if error else logging.info
        msg = LOG_TEMPLATE.format(farmer_name=self.name.lower(), 
                                  user=self.account_name, 
                                  message=message,
                                  ip=ip)
        log_method(msg)

    def error(self, message):
        self.log(message=message, error=True)

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
            try:
                self.farm()
                self.set_start_time()
            except Exception as err:
                self.error(err)
                self.start_time = time() + 60 * 60
            self.log('Следующий заход в : {}'.format(
                datetime.fromtimestamp(self.start_time).strftime('%d-%m-%Y %H:%M:%S')
            ))
