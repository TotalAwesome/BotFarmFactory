from random import random
from telethon.types import InputBotAppShortName
from bots.base.base import BaseFarmer, time
from bots.cell.strings import HEADERS, URL_PROFILE, URL_CLAIM, URL_TAP, MSG_CLAIM, MSG_PROFILE_UPDATE, \
    MSG_STATE, MSG_TAP


class BotFarmer(BaseFarmer):

    name = 'cellcoin_bot'
    upgrades = {}
    info = {}
    next_claim = None
    extra_code = "102796269"

    @property
    def initialization_data(self):
        return dict(peer='me', 
                    app=InputBotAppShortName(self.initiator.get_input_entity(self.name), "app"),
                    start_param='app')

    def set_headers(self, *args, **kwargs):
        self.headers = HEADERS.copy()

    def authenticate(self, *args, **kwargs):
        auth_data = self.initiator.get_auth_data(**self.initialization_data)['authData']
        self.headers['Authorization'] = auth_data[auth_data.index('user'):]

    def api_call(self, url, json=None):
        response = self.post(url, json=json)
        if response.status_code == 200:
            return response.json()
        else:
            return {}

    def update_profile(self):
        self.info = self.api_call(URL_PROFILE)['user']
        self.log(MSG_PROFILE_UPDATE)

    def set_start_time(self):
        taps_recover_seconds = self.info['max_energy'] / self.info['regen_rate_per_second']
        self.start_time = time() + taps_recover_seconds

    def tap(self):
        self.update_profile()
        self.info = self.api_call(URL_TAP, json={"clicks": 1})['user']
        if energy := self.info['energy']:
            self.api_call(URL_TAP, json={"clicks": energy})
        self.log(MSG_TAP.format(taps=energy / 1_000_000))

    def claim(self):
        self.update_profile()
        if not self.next_claim or self.next_claim <= time():
            balance = self.info['balance']
            if response := self.api_call(URL_CLAIM):
                self.info = response['user']
                diff = self.info['balance'] - balance
                self.next_claim = time() + 60 * 12 * self.info['storage_level']
                self.log(MSG_CLAIM.format(amount=diff / 1_000_000))


    def farm(self):
        self.tap()
        self.claim()
        self.log(MSG_STATE.format(balance=self.info['balance'] / 1_000_000))
        