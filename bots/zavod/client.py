import json
from random import random
from bots.base.utils import to_localtz_timestamp, api_response
from bots.base.base import BaseFarmer, time
from bots.zavod.strings import HEADERS, URL_INIT, URL_CALIM, URL_FARM, URL_PROFILE, MSG_CLAIM, MSG_PROFILE, MSG_STATE
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
        self.log(f'Монет: {tokens}')
        tool = self.ide['toolkitLevel']
        self.log(f'Уровень инструментов: {tool}')
        work = self.ide['workbenchLevel']
        self.log(f'Уровень верстака: {work}')
        self.log(f'Гильдия: {guild}')
        if guild == None:
            gu = self.post('https://zavod-api.mdaowallet.com/guilds/join', json={'guildId': 81,})
            self.log(f'Вступили в гильдию')
        if tool == 5 and work == 5:
            self.burn(tokens)


        if tool == 0:
            money = 100
        if tool == 1:
            money = 250
        if tool == 2:
            money = 500
        if tool == 3:
            money = 2000
        if tool == 4:
            money = 5000

        if work == 0:
            money1 = 100
        if work == 1:
            money1 = 500
        if work == 2:
            money1 = 1000
        if work == 3:
            money1 = 2500
        if work == 4:
            money1 = 7500

        if tool < 5 and tokens >= money:
            try:
                toolkit = self.post('https://zavod-api.mdaowallet.com/user/upgradeToolkit')
                self.log(f"Улучшили инструменты")
                sleep(2)
            except:
                print()
        if work < 5 and tokens >= money1:
            try:
                work = self.post('https://zavod-api.mdaowallet.com/user/upgradeWorkbench')
                self.log(f"Улучшили верстак")
                sleep(2)
            except:
                print()

        try:
            task = self.get('https://zavod-api.mdaowallet.com/missions',
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
                    except:
                        print()
                if state == "STARTED" and type == "LINK":
                    try:
                        self.link(id)
                    except:
                        print()
                if state == "STARTED" and type == "TELEGRAM":
                    try:
                        self.telegram(id)
                    except:
                        print()

        except:
            print()
    def burn(self, tokens):
        response = self.post('https://zavod-api.mdaowallet.com/guilds/burnTokens', json={f'"amount": {tokens}'})
        self.log(f"Сожгли {tokens}")


    def taskclaim(self, id):
        sleep(2)
        response = self.post(f'https://zavod-api.mdaowallet.com/missions/claim/{id}')
        self.log(f"Получили {response['prize']} За {response['name']['ru']}")

    def link(self, id):
        sleep(2)
        response = self.post(f'https://zavod-api.mdaowallet.com/missions/confirm/link/{id}')
        self.log(f"Делаем задание на {response['prize']} За {response['name']['ru']}")


    def telegram(self, id):
        sleep(2)
        response = self.post(f'https://zavod-api.mdaowallet.com/missions/confirm/telegram/{id}')
        self.log(f"Выполняем задание {response['name']['ru']}")



    def farm(self):
        self.update_profile()
        self.update_farming()
        self.claim()
        sleep(1)
        self.update_farming()
        sleep(2)
        self.up()
        self.log(MSG_STATE.format(balance=self.info['profile'].get('tokens')))
        
