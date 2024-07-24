from time import time
from random import randrange
from bots.base.base import BaseFarmer
from bots.dogs.strings import HEADERS, URL_INIT, URL_LOGIN, MSG_CURRENT_BALANCE, \
    MSG_CURRENT_FRIENDS, URL_FRIENDS, MSG_LOGIN_ERROR

DEFAULT_EST_TIME = 60 * 10
LOGIN_RANGE = (100, 1300)


class BotFarmer(BaseFarmer):
    name = "dogshouse_bot"
    balance = None
    user_id = None
    ref_code = None
    auth_data = None
    extra_code = '07wokQJZTrS5FSrah8SigQ'
    initialization_data = dict(peer=name, bot=name, url=URL_INIT, start_param=extra_code)

    def set_headers(self, *args, **kwargs):
        self.headers = HEADERS.copy()

    def authenticate(self, *args, **kwargs):
        try:

            init_data = self.initiator.get_auth_data(**self.initialization_data)
            self.auth_data = init_data['authData']
            login_url = URL_LOGIN + '?' + 'invite_hash=' + self.extra_code

            result = self.post(login_url, data=self.auth_data)

            if result.status_code == 200:
                self.handle_successful_login(result.json())
        except Exception as e:
            self.log(MSG_LOGIN_ERROR.format(e=e))
            self.is_alive = False

    def handle_successful_login(self, json_data):
        user_data = json_data
        self.balance = user_data['balance']
        self.ref_code = user_data['reference']
        self.user_id = user_data['telegram_id']
        self.is_alive = True

    def set_start_time(self):
        self.start_time = time() + DEFAULT_EST_TIME + int(randrange(*LOGIN_RANGE))

    def farm(self):
        self.show_balance()
        self.show_friends()

    def show_balance(self):
        self.log(MSG_CURRENT_BALANCE.format(balance=self.balance))

    def show_friends(self):
        url = URL_FRIENDS + f'?user_id={self.user_id}&reference={self.ref_code}'
        response = self.get(url)
        response_json = response.json()
        self.log(MSG_CURRENT_FRIENDS.format(total=response_json['count']))
