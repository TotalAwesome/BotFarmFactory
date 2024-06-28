from bots.base.utils import to_localtz_timestamp
from bots.base.base import BaseFarmer, time
from bots.timeton.strings import HEADERS, URL_AUTH, URL_INIT, URL_BONUS_CLAIM, URL_FARM_CLAIM, URL_FARM_START, \
    MSG_BONUS, MSG_CLAIM, MSG_STATE, MSG_FARM, URL_STAKING_CLAIM, URL_FRIENDS_CLAIM, MSG_FRIENDS_CLAIM, \
    MSG_STAKING_CLAIM

class BotFarmer(BaseFarmer):

    name = 'timetonbot'
    info = {}
    extra_code = "TotalAwesome"
    initialization_data = dict(peer=name, bot=name, url=URL_INIT)
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
        self.start_time = min(self.claim_time, self.ref_claim_time, self.staking_claim_time)

    @property
    def claim_time(self):
        return to_localtz_timestamp(self.info["claimDate"])

    @property
    def ref_claim_time(self):
        return to_localtz_timestamp(self.info["refClaimTime"])

    @property
    def staking_claim_time(self):
        return to_localtz_timestamp(self.info["stakingDate"])

    @property
    def bonus_claim_time(self):
        return to_localtz_timestamp(self.info["counterDateBonus"])

    def farm_claim(self):
        if self.info['claimActive'] and self.claim_time <= time():
            if response := self.api_call(URL_FARM_CLAIM, post=False):
                self.info = response['data']
                self.log(MSG_CLAIM)
    
    def ref_claim(self):
        if self.ref_claim_time <= time():
            if response := self.api_call(URL_FRIENDS_CLAIM, post=False):
                self.info = response["data"]
                self.log(MSG_FRIENDS_CLAIM)
    
    def staking_claim(self):
        if self.staking_claim_time <= time():
            if response := self.api_call(URL_STAKING_CLAIM, post=False):
                self.info = response["data"]
                self.log(MSG_STAKING_CLAIM)

    def claim_bonus(self):
        if self.bonus_claim_time <= time():
            if response := self.api_call(URL_BONUS_CLAIM, post=False):
                self.info = response["data"]
                self.log(MSG_BONUS)
            
    def start_farm(self):
        if not self.info['claimActive']:
            if response := self.api_call(URL_FARM_START, post=False):
                self.info = response['data']
                self.log(MSG_FARM)


    def farm(self):
        self.claim_bonus()
        self.farm_claim()
        self.start_farm()
        self.ref_claim()
        self.staking_claim()
        self.log(MSG_STATE.format(balance=self.info['balance']))
        
