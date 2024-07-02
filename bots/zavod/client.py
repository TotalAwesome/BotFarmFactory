from random import random
from bots.base.utils import to_localtz_timestamp, api_response
from bots.base.base import BaseFarmer, time
from bots.zavod.strings import HEADERS, URL_INIT, URL_CALIM, URL_FARM, URL_PROFILE, MSG_CLAIM, MSG_PROFILE, MSG_STATE


class BotFarmer(BaseFarmer):

    name = 'Mdaowalletbot'
    extra_code = "102796269"
    info = dict(profile={}, farming={})
    initialization_data = dict(peer=name, bot=name, url=URL_INIT)
    payload_base = {}
    codes_to_refresh = (400,)
    refreshable_token = True

    def set_headers(self, *args, **kwargs):
        self.headers = HEADERS.copy()
        self.get = api_response(super().get)
        self.post = api_response(super().post)
        self.delete = api_response(super().delete)

    def authenticate(self, *args, **kwargs):
        auth_data = self.initiator.get_auth_data(**self.initialization_data)['authData']
        self.headers['telegram-init-data'] = auth_data

    def refresh_token(self):
        self.authenticate()

    def set_start_time(self):
        self.start_time = self.claim_date + int(random() * 10)

    def update_profile(self):
        if result := self.get(URL_PROFILE):
            self.info['profile'] = result
            self.log(MSG_PROFILE)
    
    def update_farming(self):
        if result := self.get(URL_FARM):
            self.info['farming'] = result

    @property
    def claim_date(self):
        last_claim = to_localtz_timestamp(self.info['farming'].get('lastClaim'))
        next_claim = last_claim + self.info['farming'].get('claimInterval') / 1000
        return next_claim

    def claim(self):
        if time() >= self.claim_date:
            if result := self.post(URL_CALIM):
                self.info['profile'] = result
                self.log(MSG_CLAIM)

    def farm(self):
        self.update_profile()
        self.update_farming()
        self.claim()
        self.update_farming()
        self.log(MSG_STATE.format(balance=self.info['profile'].get('tokens')))
        
