from telethon.types import InputBotAppShortName
from bots.base.utils import to_localtz_timestamp, api_response
from bots.base.base import BaseFarmer, time
from bots.anon.strings import HEADERS, URL_VERIFY, URL_VERIFICATION, URL_CLAIMED, URL_CLAIM, \
    URL_INIT, MSG_CLAIM, MSG_STATE


class BotFarmer(BaseFarmer):

    name = 'anonearnbot'
    info = {}
    app_extra = 'iDb64mAALgfaXGj8gTCDZ1'
    payload_base = {}
    codes_to_refresh = (403,)
    refreshable_token = True

    @property
    def initialization_data(self):
        return dict(peer=self.name, 
                    app=InputBotAppShortName(self.initiator.get_input_entity(self.name), "app"),
                    start_param=self.app_extra)

    def set_headers(self, *args, **kwargs):
        self.headers = HEADERS.copy()
        self.get = api_response(super().get)
        self.post = api_response(super().post)
        self.delete = api_response(super().delete)

    def refresh_token(self, *args, **kwargs):
        self.initiator.connect()
        self.authenticate()
        self.initiator.disconnect()

    def authenticate(self, *args, **kwargs):
        auth_data = self.initiator.get_auth_data(**self.initialization_data)['authData']
        payload = {"hash": auth_data}
        self.headers['Anon-Auth'] = auth_data
        if self.post(URL_VERIFY, json=payload):
            if response := self.post(URL_VERIFICATION, json=payload):
                if token := response["data"]["accessToken"]:
                    self.headers['Authorization'] = f'Bearer {token}'
                else:
                    self.error(f"{self.name} не зарегистрирован по рефке")
                    self.is_alive = False

    def set_start_time(self):
        self.start_time = time() + self.info.get('claimSecondsAvailable', 300)

    @property
    def claim_date(self):
        return to_localtz_timestamp(self.info['claimDate'])

    def claim(self):
        if claimed := self.get(URL_CLAIMED):
            self.info = claimed.get('data', {})
            if self.info.get('isButtonEnabled'):
                if response := self.post(URL_CLAIM):
                    self.info = response.get('data', {})
                    self.log(MSG_CLAIM)

    def farm(self):
        self.claim()
        self.log(MSG_STATE.format(balance=self.info.get('personalXPBalance')))
        