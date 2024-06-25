from telethon.types import InputBotAppShortName
from bots.base.base import BaseFarmer, time

from bots.cell.strings import HEADERS, URL_PROFILE, URL_CLAIM, URL_TAP, MSG_CLAIM, MSG_PROFILE_UPDATE, \
    MSG_STATE, MSG_TAP, URL_LEVELS, MSG_LEVELS_UPDATE


class BotFarmer(BaseFarmer):

    name = 'cellcoin_bot'
    upgrades = {}
    info = {}
    levels = {}
    next_claim = None
    extra_code = "102796269"

    @property
    def initialization_data(self):
        return dict(peer=self.name, 
                    app=InputBotAppShortName(self.initiator.get_input_entity(self.name), "app"),
                    start_param='')

    def set_headers(self, *args, **kwargs):
        self.headers = HEADERS.copy()

    def authenticate(self, *args, **kwargs):
        auth_data = self.initiator.get_auth_data(**self.initialization_data)['authData']
        self.headers['Authorization'] = auth_data[auth_data.index('user'):]

    def api_call(self, url, post=True, json=None):
        method = self.post if post else self.get
        kwargs = dict(url=url)
        if post:
            kwargs['json'] = json
        response = method(**kwargs)
        if response.status_code == 200:
            return response.json()
        else:
            return {}

    @property
    def energy_max(self):
        level = str(self.info['energy_level'])
        return self.levels['cell_energy_levels_map'][level]['capacity']

    def update_profile(self):
        self.info = self.api_call(URL_PROFILE, post=False).get("cell", {})
        self.log(MSG_PROFILE_UPDATE)

    def update_levels(self):
        self.levels = self.api_call(URL_LEVELS, post=False)
        self.log(MSG_LEVELS_UPDATE)

    def set_start_time(self):
        taps_recover_seconds = self.energy_max / self.info['energy_regen_rate']
        self.start_time = time() + taps_recover_seconds

    def tap(self):
        self.update_profile()
        balance = self.info['balance']
        self.info = self.api_call(URL_TAP, json={"clicks_amount": 1})['cell']
        if energy := self.info.get("energy_amount"):
            clicks_amount = energy // self.info["click_energy_cost"]
            self.info = self.api_call(URL_TAP, json={"clicks_amount": clicks_amount})['cell']
        self.log(MSG_TAP.format(taps=clicks_amount * self.info["click_energy_cost"]))

    def claim(self):
        self.update_profile()
        if not self.next_claim or self.next_claim <= time():
            balance = self.info['balance']
            if response := self.api_call(URL_CLAIM):
                self.info = response['cell']
                diff = self.info['balance'] - balance
                self.next_claim = time() + 60 * 12 * self.info['storage_level']
                self.log(MSG_CLAIM.format(amount=diff / 1_000_000))


    def farm(self):
        self.update_levels()
        self.tap()
        self.claim()
        self.log(MSG_STATE.format(balance=self.info['balance'] / 1_000_000))
        