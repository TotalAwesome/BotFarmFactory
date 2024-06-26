from random import random
from datetime import datetime
from bots.base.utils import to_localtz_timestamp
from bots.base.base import BaseFarmer, time
from bots.timeton.strings import HEADERS, URL_AUTH, URL_INIT, URL_BONUS_CLAIM, URL_FARM_CLAIM, URL_FARM_START, \
    MSG_BONUS, MSG_CLAIM, MSG_STATE, MSG_FARM

class BotFarmer(BaseFarmer):

    name = 'timetonbot'
    info = {}
    extra_code = "TotalAwesome"
    initialization_data = dict(peer=name, bot=name, url=URL_INIT)
    bonus_claimed_date = None
    payload_base = {}

    def set_headers(self, *args, **kwargs):
        self.headers = HEADERS.copy()

    def authenticate(self, *args, **kwargs):
        auth_data = self.initiator.get_auth_data(**self.initialization_data)['authData']
        self.payload_base = {"telegramData": auth_data}
        self.info = self.api_call(URL_AUTH, json=self.payload_base)['data']

    def api_call(self, url, post=True, json=None):
        if post:
            response = self.post(url, json=json)
        else:
            response = self.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {}

    def set_start_time(self):
        self.start_time = self.claim_date + 5

    @property
    def claim_date(self):
        return to_localtz_timestamp(self.info['claimDate'])

    def claim(self):
        if self.info['claimActive'] and self.claim_date <= time():
            if response := self.api_call(URL_FARM_CLAIM, post=False):
                self.info = response['data']
                self.log(MSG_CLAIM)
    
    def start_farm(self):
        if not self.info['claimActive']:
            if response := self.api_call(URL_FARM_START, post=False):
                self.info = response['data']
                self.log(MSG_FARM)

    def claim_bonus(self):
        today = datetime.now().date()
        if not self.bonus_claimed_date or today > self.bonus_claimed_date:
            if result := self.api_call(URL_BONUS_CLAIM, post=False):
                self.log(MSG_BONUS)
            self.bonus_claimed_date = today

    def farm(self):
        self.claim_bonus()
        self.claim()
        self.start_farm()
        self.log(MSG_STATE.format(balance=self.info['balance']))
        