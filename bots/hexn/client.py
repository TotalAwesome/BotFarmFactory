import hashlib
import random
from time import time

from bots.base.base import BaseFarmer
from bots.hexn.strings import HEADERS, URL_INIT, URL_LOGIN, URL_START_FARMING, MSG_REFRESH, URL_REFRESH_TOKEN, \
    MSG_FARMING_STARTED, MSG_FARMING_ALREADY_STARTED, MSG_FARMING_ERROR, MSG_UNKNOWN_RESPONSE

DEFAULT_EST_TIME = 60 * 10


class BotFarmer(BaseFarmer):
    name = "hexn_bot"
    codes_to_refresh = (401,)
    refreshable_token = True
    auth_data = None
    balance = None
    end_time = None

    initialization_data = dict(peer=name, bot=name, url=URL_INIT)

    def set_headers(self, *args, **kwargs):
        self.headers = HEADERS.copy()

    def authenticate(self, *args, **kwargs):
        init_data = self.initiator.get_auth_data(**self.initialization_data)

        data = {
            'initial_data': init_data['authData'],
            'telegram_user_id': init_data['userId'],
            'fingerprint': self.generate_fingerprint(),
            'platform': 'WEB',
            'locale': 'en'
        }

        result = self.post(URL_LOGIN, json=data)

        if result.status_code == 200:
            self.auth_data = result.json()['data']

            self.headers['Access-Token'] = self.auth_data['jwt_access_token']
            self.is_alive = True

    def set_start_time(self):
        if self.end_time:
            self.start_time = self.end_time
        else:
            est_time = DEFAULT_EST_TIME
            self.start_time = time() + est_time

    def start_farming(self):
        data = {
            'platform': 'WEB',
        }
        result = self.post(URL_START_FARMING, json=data)

        if result.status_code == 200:
            response_json = result.json()

            error = response_json.get('error')
            data = response_json.get('data')

            if error:
                error_code = error.get('code')
                if error_code == 'PENDING_FARMING_EXISTS':
                    self.log(MSG_FARMING_ALREADY_STARTED)
                    farming_details = error.get('details', {}).get('farming', {})
                    self.end_time = farming_details.get('end_at', 0) // 1000
                else:
                    self.log(MSG_FARMING_ERROR)
            elif data:
                self.log(MSG_FARMING_STARTED)
                self.end_time = data.get('end_at', 0) // 1000
            else:
                self.log(MSG_UNKNOWN_RESPONSE)

    def refresh_token(self):
        self.log(MSG_REFRESH)
        self.headers.pop('Access-Token')
        result = self.post(URL_REFRESH_TOKEN, json={"refresh": self.auth_data['jwt_refresh_token']})
        if result.status_code == 200:
            self.auth_data = result.json()
            self.headers['Access-Token'] = self.auth_data['jwt_access_token']

    @staticmethod
    def generate_fingerprint():
        random_bytes = random.getrandbits(128).to_bytes(16, byteorder='big')
        hash_object = hashlib.md5(random_bytes)
        hex_string = hash_object.hexdigest()

        return hex_string

    def farm(self):
        self.start_farming()
