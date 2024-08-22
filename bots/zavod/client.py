import json
from random import random
from bots.base.utils import to_localtz_timestamp, api_response
from bots.base.base import BaseFarmer, time
from bots.zavod.strings import HEADERS, URL_INIT, URL_CALIM, URL_FARM, URL_PROFILE, MSG_CLAIM, MSG_PROFILE, MSG_STATE, URL_UPGRADE_TOOLKIT, URL_UPGRADE_WORKBENCH, URL_BURN_TOKENS, URL_MISSIONS, URL_CLAIM_MISSION, URL_CONFIRM_LINK_MISSION, URL_CONFIRM_TELEGRAM_MISSION, \
    MSG_TOKENS, MSG_TOOLKIT_LEVEL, MSG_WORKBENCH_LEVEL, MSG_GUILD, MSG_JOINED_GUILD, MSG_UPGRADED_TOOLKIT, MSG_UPGRADED_WORKBENCH, MSG_BURNED_TOKENS, MSG_CLAIMED_MISSION, MSG_LINK_MISSION, MSG_TELEGRAM_MISSION, MSG_ERROR_UPGRADING_TOOLKIT, MSG_ERROR_UPGRADING_WORKBENCH, MSG_ERROR_BURNING_TOKENS, MSG_ERROR_FETCHING_MISSIONS, MSG_ERROR_CLAIMING_MISSION, MSG_ERROR_CONFIRMING_LINK_MISSION, MSG_ERROR_CONFIRMING_TELEGRAM_MISSION
from time import sleep
import requests

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
        next_claim = last_claim + self.info['farming'].get('claimInterval') / 1000
        return next_claim

    def claim(self):
        if time() >= self.claim_date:
            if result := self.post(URL_CALIM):
                self.info['profile'] = result
                self.log(MSG_CLAIM)

    def up(self):
        guild = self.info['profile']['guildId']
        self.ide = self.get('https://zavod-api.mdaowallet.com/user/farm')
        tokens = self.info['profile']['tokens']
        self.log(MSG_TOKENS.format(tokens=tokens))
        tool = self.ide['toolkitLevel']
        self.log(MSG_TOOLKIT_LEVEL.format(tool=tool))
        work = self.ide['workbenchLevel']
        self.log(MSG_WORKBENCH_LEVEL.format(work=work))
        self.log(MSG_GUILD.format(guild=guild))
        if guild is None:
            self.post('https://zavod-api.mdaowallet.com/guilds/join', json={'guildId': 81,})
            self.log(MSG_JOINED_GUILD)

        # Upgrade logic based on tool and workbench levels
        self.upgrade_tool(tool, tokens)
        self.upgrade_workbench(work, tokens)

        if tool == 5 and work == 49:
            self.burn(tokens)

        self.process_missions()  # Add missions processing

    def upgrade_tool(self, tool, tokens):
        cost = {
            0: 100,
            1: 250,
            2: 500,
            3: 2000,
            4: 5000
        }.get(tool, float('inf'))  # Default to infinity if tool is out of range

        if tokens >= cost and tool < 5:  # Check for tool level first
            try:
                response = self.post(URL_UPGRADE_TOOLKIT)
                self.log(MSG_UPGRADED_TOOLKIT)
                sleep(2)
                self.info['profile']['tokens'] = tokens - cost
            except Exception as e:
                self.log(MSG_ERROR_UPGRADING_TOOLKIT.format(error=e))

    def upgrade_workbench(self, work, tokens):
        cost = {
            0: 50,
            1: 200,
            2: 500,
            3: 2000,
            4: 5000,
            5: 7500,
            6: 12500,
            7: 15000,
            8: 17500,
            9: 20000,
            10: 25000,
            11: 30000,
            12: 35000,
            13: 40000,
            14: 50000,
            15: 60000,
            16: 70000,
            17: 80000,
            18: 100000,
            19: 120000,
            20: 140000,
            21: 160000,
            22: 200000,
            23: 240000,
            24: 280000,
            25: 320000,
            26: 400000,
            27: 480000,
            28: 560000,
            29: 640000,
            30: 800000,
            31: 960000,
            32: 1120000,
            33: 1280000,
            34: 1600000,
            35: 1920000,
            36: 2240000,
            37: 2560000,
            38: 3200000,
            39: 4480000,
            40: 5120000,
            41: 6400000,
            42: 7680000,
            43: 8960000,
            44: 10240000,
            45: 12800000,
            46: 15360000,
            47: 17920000,
            48: 20480000,
            49: 25600000
        }.get(work, float('inf'))

        if tokens >= cost and work < 5:
            try:
                self.post(URL_UPGRADE_WORKBENCH)
                self.log(MSG_UPGRADED_WORKBENCH)
                sleep(2)
                self.info['profile']['tokens'] = tokens - cost
            except Exception as e:
                self.log(MSG_ERROR_UPGRADING_WORKBENCH.format(error=e))

    def burn(self, tokens):
        try:
            response = self.post(URL_BURN_TOKENS, json={"amount": tokens})
            self.log(MSG_BURNED_TOKENS.format(tokens=tokens))
        except Exception as e:
            self.log(MSG_ERROR_BURNING_TOKENS.format(error=e))

    def process_missions(self):
        try:
            task = self.get(URL_MISSIONS,
                params={
                        'offset': '0',
                        'status': 'ACTIVE',
                        }
                            )
            #print(json.dumps(task, indent=4))
            for q in task['missions']:
                id = q['id']
                state = q['state']
                type = q['type']
                if state == 'READY_TO_CLAIM':
                    try:
                        self.taskclaim(id)
                    except Exception as e:
                        self.log(MSG_ERROR_CLAIMING_MISSION.format(id=id, error=e))
                if state == "STARTED" and type == "LINK":
                    try:
                        self.link(id)
                    except Exception as e:
                        self.log(MSG_ERROR_CONFIRMING_LINK_MISSION.format(id=id, error=e))
                if state == "STARTED" and type == "TELEGRAM_CHANNEL":
                    try:
                        self.telegram(id)
                    except Exception as e:
                        self.log(MSG_ERROR_CONFIRMING_TELEGRAM_MISSION.format(id=id, error=e))

        except Exception as e:
            self.log(MSG_ERROR_FETCHING_MISSIONS.format(error=e))

    def taskclaim(self, id):
        sleep(2)
        try:
            response = self.post(f'{URL_CLAIM_MISSION}{id}')
            self.log(MSG_CLAIMED_MISSION.format(prize=response['prize'], name=response['name']['ru']))
        except Exception as e:
            self.log(MSG_ERROR_CLAIMING_MISSION.format(id=id, error=e))

    def link(self, id):
        sleep(2)
        try:
            response = self.post(f'{URL_CONFIRM_LINK_MISSION}{id}')
            self.log(MSG_LINK_MISSION.format(prize=response['prize'], name=response['name']['ru']))
        except Exception as e:
            self.log(MSG_ERROR_CONFIRMING_LINK_MISSION.format(id=id, error=e))

    def telegram(self, id):
        sleep(2)
        try:
            response = self.post(f'{URL_CONFIRM_TELEGRAM_MISSION}{id}')
            self.log(MSG_TELEGRAM_MISSION.format(name=response['name']['ru']))
        except Exception as e:
            self.log(MSG_ERROR_CONFIRMING_TELEGRAM_MISSION.format(id=id, error=e))

    def farm(self):
        self.update_profile()
        self.update_farming()
        self.claim()
        sleep(1)
        self.update_farming()
        sleep(2)
        self.up()
