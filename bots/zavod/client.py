import json
import random
import requests
from bots.base.utils import to_localtz_timestamp, api_response
from bots.base.base import BaseFarmer, time
from bots.zavod.strings import HEADERS, URL_INIT, URL_CLAIM, URL_FARM, URL_PROFILE, MSG_CLAIM, MSG_PROFILE, \
    URL_UPGRADE_TOOLKIT, URL_UPGRADE_WORKBENCH, URL_BURN_TOKENS, URL_MISSIONS, URL_CLAIM_MISSION, \
    URL_CONFIRM_LINK_MISSION, URL_CONFIRM_TELEGRAM_MISSION, \
    MSG_TOKENS, MSG_TOOLKIT_LEVEL, MSG_WORKBENCH_LEVEL, MSG_GUILD, MSG_JOINED_GUILD, MSG_UPGRADED_TOOLKIT, \
    MSG_UPGRADED_WORKBENCH, MSG_BURNED_TOKENS, MSG_CLAIMED_MISSION, MSG_LINK_MISSION, MSG_TELEGRAM_MISSION, \
    MSG_ERROR_UPGRADING_TOOLKIT, MSG_ERROR_UPGRADING_WORKBENCH, MSG_ERROR_BURNING_TOKENS, MSG_ERROR_FETCHING_MISSIONS, \
    MSG_ERROR_CLAIMING_MISSION, MSG_ERROR_CONFIRMING_LINK_MISSION, MSG_ERROR_CONFIRMING_TELEGRAM_MISSION, \
    URL_WORKBENCH_SETTINGS, URL_TOOLKIT_SETTINGS, URL_GUILD_JOIN
from time import sleep


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
        self.start_time = self.claim_date + random.randint(0, 9)

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
            if result := self.post(URL_CLAIM, return_codes=(500,)):
                self.info['profile'] = result
                self.log(MSG_CLAIM)

    def up(self):
        guild = self.info['profile']['guildId']
        self.ide = self.get(URL_FARM)
        tokens = round(self.info['profile']['tokens'])
        self.log(MSG_TOKENS.format(tokens=tokens))
        tool = self.ide['toolkitLevel']
        self.log(MSG_TOOLKIT_LEVEL.format(tool=tool))
        work = self.ide['workbenchLevel']
        self.log(MSG_WORKBENCH_LEVEL.format(work=work))
        self.log(MSG_GUILD.format(guild=guild))
        if guild is None:
            self.post(URL_GUILD_JOIN, json={'guildId': 81, })
            self.log(MSG_JOINED_GUILD)

        self.upgrade_tool(tool, tokens)
        self.upgrade_workbench(work, tokens)

        if tool == 5 and work == 49:
            self.burn(tokens)

    def upgrade_tool(self, tool, tokens):
        tool += 1
        toolkit_settings = self.get(URL_TOOLKIT_SETTINGS)
        cost = {item['level']: item['price'] for item in toolkit_settings}
        if tokens >= cost.get(tool, float('inf')) and tool < 5:  # Check for tool level first
            try:
                self.post(URL_UPGRADE_TOOLKIT)
                self.log(MSG_UPGRADED_TOOLKIT)
                sleep(2)
                self.info['profile']['tokens'] = tokens - cost.get(tool, 0)
            except Exception as e:
                self.log(MSG_ERROR_UPGRADING_TOOLKIT.format(error=e))

    def upgrade_workbench(self, work, tokens):
        work += 1
        workbench_settings = self.get(URL_WORKBENCH_SETTINGS)
        cost = {item['level']: item['price'] for item in workbench_settings}
        if tokens >= cost.get(work, float('inf')) and work < 49:
            try:
                self.post(URL_UPGRADE_WORKBENCH)
                self.log(MSG_UPGRADED_WORKBENCH)
                sleep(2)
                self.info['profile']['tokens'] = tokens - cost.get(work, 0)
            except Exception as e:
                self.log(MSG_ERROR_UPGRADING_WORKBENCH.format(error=e))

    def burn(self, tokens):
        try:
            self.post(URL_BURN_TOKENS, json={"amount": tokens})
            self.log(MSG_BURNED_TOKENS.format(tokens=tokens))
        except Exception as e:
            self.log(MSG_ERROR_BURNING_TOKENS.format(error=e))

    def process_missions(self):
        try:
            task = self.get(URL_MISSIONS, params={
                                'offset': '0',
                                'status': 'ACTIVE',
                            }
                            )
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
            response = self.post(f'{URL_CLAIM_MISSION}{id}', return_codes=(403,))
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

    def game_init(self):
        response = requests.get('https://zavod-api.mdaowallet.com/craftGame', headers=self.headers)
        if response.status_code == 200:
            sleep(2)
            self.game()
    def game(self):
        self.log('Я хочу сыграть с тобой в игру :)')
        numbers = random.sample(range(20), 3)
        a, b, c = numbers
        json_data = {
            'selectedSells': [
                a,
                b,
                c,
            ],
            'action': 'SAVE',
        }

        response = requests.post(
            'https://zavod-api.mdaowallet.com/craftGame/finishLevel',
            headers=self.headers,
            json=json_data
        )
        if response.status_code != 200:
            test = response.json()
            print(json.dumps(test, indent=4))

        if response.status_code == 200:
            game_data = response.json()
            if game_data['level'] > 0:
                self.log(f"Выиграли lvl: {game_data['level']}")
                sleep(3)
                self.game()
            elif game_data['level'] == 0:
                self.log('Ты проиграл')
        elif response.status_code == 403:
            self.log('Рано еще играть')

        elif response.status_code != 200:
            print(json.dumps(response, indent=4))

    def farm(self):
        self.update_profile()
        sleep(1)
        self.update_farming()
        sleep(1)
        self.process_missions()
        sleep(1)
        self.claim()
        sleep(1)
        self.update_farming()
        sleep(1)
        self.up()
        sleep(1)
        self.game_init()
