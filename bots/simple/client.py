from random import random, randrange
from bots.base.base import BaseFarmer
from time import time, sleep
from bots.simple.utils import get_sorted_upgrades
from bots.simple.config import BUY_UPGRADES
from bots.simple.strings import HEADERS, URL_INIT, URL_PROFILE, URL_TAP, URL_GET_MINING_BLOCKS, URL_FRIENDS, \
    URL_GET_TASK_LIST, URL_CLAIM_FARMED, URL_START_FARM, URL_CHECK_TASK, URL_START_TASK, URL_CLAIM_FRIENDS, \
    URL_BUY_UPGRADE, URL_CLAIM_SPIN, MSG_PROFILE_UPDATE, MSG_TAP, MSG_START_FARMING, MSG_BUY_UPGRADE, SPIN_TYPES, \
    MSG_SPIN, MSG_START_TASK, MSG_CLAIM_FARM, MSG_CLAIM_REFS, MSG_STATE


class BotFarmer(BaseFarmer):

    name = 'simple_tap_bot'

    initialization_data = dict(peer=name, bot=name, url=URL_INIT)
    payload_base = {'userId': None, 'authData': None, }
    initiator = None
    upgrades = {}
    info = {}
    extra_code = "1718085881160"

    def set_headers(self, *args, **kwargs):
        self.headers = HEADERS.copy()

    def authenticate(self, *args, **kwargs):
        self.payload_base = self.initiator.get_auth_data(**self.initialization_data)

    def api_call(self, url, payload=None):
        payload = payload or self.payload_base
        result = self.post(url, json=payload)
        if result.status_code == 200:
            return result.json()
        else:
            self.log(str(result.status_code) + ' ' + result.text)
            return {}

    def update_profile(self):
        self.info = self.api_call(URL_PROFILE).get('data', {})
        self.log(MSG_PROFILE_UPDATE)

    @property
    def mine_per_hour(self):
        return self.info['activeFarmingPerSec'] * 3600

    @property
    def taps_per_hour(self):
        return self.info['addTapPerSecond'] * 3600

    def set_start_time(self):
        taps_recover_seconds = self.info.get('maxAvailableTaps') / self.info.get('addTapPerSecond')
        farming_seconds = self.info['maxFarmingSecondSec'] - self.info['activeFarmingSeconds']
        self.start_time = time() + min(taps_recover_seconds, farming_seconds)

    def tap(self):
        if available_taps := self.info['availableTaps']:
            if taps := int((available_taps // self.info['tapSize']) * self.info['tapSize']):
                payload = self.payload_base.copy()
                payload['count'] = taps
                self.api_call(URL_TAP, payload=payload)
                self.log(MSG_TAP.format(taps=taps))

    def start_task(self, task_id, task_type):
        payload = self.payload_base.copy()
        payload.update(dict(id=task_id, type=task_type))
        self.api_call(URL_START_TASK, payload=payload)
        self.log(MSG_START_TASK)
        

    def check_task(self, task_id, task_type):
        payload = self.payload_base.copy()
        payload.update(dict(id=task_id, type=task_type))
        self.api_call(URL_CHECK_TASK, payload=payload)
        

    def buy_upgrade(self, upgrade):
        level = upgrade['currentLevel'] + 1
        mine_id = upgrade['mineId']
        payload = self.payload_base.copy()
        payload.update(dict(level=level, mineId=mine_id))
        self.update_profile()
        if self.info['balance'] >= upgrade['nextPrice']:
            self.api_call(URL_BUY_UPGRADE, payload=payload)
            self.log(MSG_BUY_UPGRADE.format(
                name=upgrade['mineId'],
                level=upgrade['currentLevel'] + 1,
                price=upgrade['nextPrice'],
                payback=upgrade['payback'],
                ))
            return True
        else:
            return False

    def claim_spin(self):
        for _ in range(self.info.get('spinCount', 0)):
            payload = self.payload_base.copy()
            payload.update(dict(amount=0, frontCoef=random() * 1000))
            result = self.api_call(URL_CLAIM_SPIN, payload=payload)
            tap_type = SPIN_TYPES.get(result['data']['spinType'], 
                                      result['data']['spinType'])
            self.log(MSG_SPIN.format(type=tap_type,
                                     amount=result['data']['amount']))
            sleep(randrange(1, 5))
                             
    def update_upgrades(self):
        self.upgrades = self.api_call(URL_GET_MINING_BLOCKS).get('data', {}).get('mines', [])

    def friends(self):
        self.api_call(URL_FRIENDS)

    def tasks(self):
        self.api_call(URL_GET_TASK_LIST)

    def start_farm(self):
        if self.info['activeFarmingSeconds'] == 0 and self.info['activeFarmingBalance'] == 0:
            self.api_call(URL_START_FARM)
            self.log(MSG_START_FARMING)
            self.update_profile()

    def claim_farmed(self):
        if self.info['activeFarmingSeconds'] == self.info['maxFarmingSecondSec']:
            self.api_call(URL_CLAIM_FARMED)
            self.log(MSG_CLAIM_FARM.format(amount=self.info['activeFarmingBalance']))
            self.start_farm()
            self.update_profile()

    def claim_friends(self):
        if claimed := self.info.get('refBalance'):
            self.api_call(URL_CLAIM_FRIENDS)
            self.log(MSG_CLAIM_REFS.format(amount=claimed))

    def buy_taplimit_upgrade(self):
        self.update_upgrades()
        if upgrades_to_buy := get_sorted_upgrades(self.upgrades, upgrade_type=1):
            upgrade = upgrades_to_buy[0]
            self.buy_upgrade(upgrade)

    def buy_upgrades(self):
        while True:
            self.update_upgrades()
            if upgrades_to_buy := get_sorted_upgrades(self.upgrades):
                upgrade = upgrades_to_buy[0]
                if not self.buy_upgrade(upgrade):
                    break
                sleep(1)
            else:
                break

    def farm(self):
        self.update_profile()
        self.tap()
        self.claim_farmed()
        self.start_farm()
        self.claim_friends()
        self.claim_spin()
        if BUY_UPGRADES:
            self.buy_upgrades()
            self.buy_taplimit_upgrade()
        self.update_profile()
        self.log(MSG_STATE.format(balance=self.info['balance'],
                                  mine_per_hour=self.mine_per_hour,
                                  taps_per_hour=self.taps_per_hour))
