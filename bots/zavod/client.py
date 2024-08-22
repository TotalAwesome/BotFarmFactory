from random import random
from time import sleep
from bots.base.base import BaseFarmer, time
from bots.base.utils import to_localtz_timestamp, api_response
from bots.zavod.strings import HEADERS, URL_INIT, URL_PROFILE, URL_FARM, URL_CALIM, URL_GUILDS_JOIN, URL_USER_FARM, \
    URL_UPGRADE_TOOLKIT, URL_UPGRADE_WORKBENCH, \
    MSG_JOIN_GUILD, MSG_UPGRADE_TOOLKIT, MSG_UPGRADE_WORKBENCH, \
    MSG_NO_GUILD, MSG_LOG_COINS, MSG_LOG_TOOLKIT_LEVEL, MSG_LOG_WORKBENCH_LEVEL, MSG_PROFILE, MSG_CLAIM, \
    MSG_STATE


class BotFarmer(BaseFarmer):
    name = 'Mdaowalletbot'
    extra_code = "102796269"
    info = {'profile': {}, 'farming': {}}
    initialization_data = {'peer': name, 'bot': name, 'url': URL_INIT}
    payload_base = {}
    codes_to_refresh = (400,)
    refreshable_token = True

    def set_headers(self, *args, **kwargs):
        self.headers = HEADERS.copy()
        self.get = api_response(super().get)
        self.post = api_response(super().post)
        self.delete = api_response(super().delete)

    def authenticate(self):
        auth_data = self.initiator.get_auth_data(**self.initialization_data)['authData']
        self.headers['telegram-init-data'] = auth_data

    def refresh_token(self):
        self.initiator.connect()
        self.authenticate()
        self.initiator.disconnect()

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
        return last_claim + self.info['farming'].get('claimInterval', 0) / 1000

    def claim(self):
        if time() >= self.claim_date and (result := self.post(URL_CALIM)):
            self.info['profile'] = result
            self.log(MSG_CLAIM)

    def up(self):
        guild = self.info['profile'].get('guildId')
        ide = self.get(URL_FARM)
        tokens = self.info['profile'].get('tokens', 0)

        self.log(f'Монет: {tokens}')
        toolkit_level = ide.get('toolkitLevel', 0)
        workbench_level = ide.get('workbenchLevel', 0)
        self.log(f'Уровень инструментов: {toolkit_level}')
        self.log(f'Уровень верстака: {workbench_level}')
        self.log(f'Гильдия: {guild}')

        if guild is None:
            self.post(URL_GUILDS_JOIN, json={'guildId': 81})
            self.log(MSG_JOIN_GUILD)

        """if toolkit_level == 5 and workbench_level == 5:
            self.burn(tokens)"""

        toolkit_costs = [100, 250, 500, 2000, 5000]
        workbench_costs = [100, 500, 1000, 2500, 7500]

        if toolkit_level < len(toolkit_costs) and tokens >= toolkit_costs[toolkit_level]:
            self._upgrade('toolkit')

        if workbench_level < len(workbench_costs) and tokens >= workbench_costs[workbench_level]:
            self._upgrade('workbench')

    def _upgrade(self, upgrade_type):
        try:
            if upgrade_type == 'toolkit':
                self.post(URL_UPGRADE_TOOLKIT)
                self.log(MSG_UPGRADE_TOOLKIT)
            elif upgrade_type == 'workbench':
                self.post(URL_UPGRADE_WORKBENCH)
                self.log(MSG_UPGRADE_WORKBENCH)
            sleep(2)
        except Exception as e:
            print(f"Ошибка при улучшении {upgrade_type}: {e}")

    def farm(self):
        self.update_profile()
        self.update_farming()
        self.claim()
        sleep(1)
        self.update_farming()
        sleep(2)
        self.up()
        self.log(MSG_STATE.format(balance=self.info['profile'].get('tokens')))
