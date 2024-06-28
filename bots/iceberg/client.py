from random import random
from time import time
from bots.base.base import BaseFarmer
from bots.base.utils import to_localtz_timestamp, api_response
from bots.iceberg.strings import HEADERS, URL_BALANCE, URL_FARMING, URL_INIT, \
    MSG_CLAIM, MSG_FARM, MSG_PROFILE, MSG_STATE, URL_CLAIM_FARM


class BotFarmer(BaseFarmer):
    name = "icebergappbot"
    info = {}
    extra_code = "referral_102796269"
    initialization_data = dict(peer=name, bot=name, url=URL_INIT)
    payload_base = {}

    @property
    def claim_time(self):
        date_str = self.info.get("farming", {}).get("stop_time")
        return to_localtz_timestamp(date_str) if date_str else time() - 10 # При первом фарме, нет данных

    def set_headers(self, *args, **kwargs):
        self.headers = HEADERS.copy()
        self.get = api_response(super().get)
        self.post = api_response(super().post)
        self.delete = api_response(super().delete)

    def authenticate(self, *args, **kwargs):
        auth_data = self.initiator.get_auth_data(**self.initialization_data)["authData"]
        self.headers["x-telegram-auth"] = auth_data

    def update_profile(self):
        if response := self.get(URL_FARMING):
            self.info['farming'] = response
        if response := self.get(URL_BALANCE):
            self.info["balance"] = response
        self.log(MSG_PROFILE)

    def set_start_time(self):
        self.start_time = self.claim_time + random() * 10

    def claim(self):
        if self.claim_time <= time():
            if response := self.delete(URL_CLAIM_FARM):
                self.log(MSG_CLAIM)

    def start_farm(self):
        self.update_profile()
        if self.claim_time <= time() and self.info.get("farming", {}).get("amount", 0) == 0:
            if response := self.post(URL_FARMING):
                self.info['farming'] = response
                self.log(MSG_FARM)

    def farm(self):
        self.start_farm()
        self.claim()
        self.log(MSG_STATE.format(balance=self.info["balance"]["amount"]))
