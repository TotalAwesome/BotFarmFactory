import json
from time import sleep
from random import random
from telethon.types import InputBotAppShortName
from bots.base.base import BaseFarmer, time
from bots.base.utils import api_response, to_localtz_timestamp
from urllib.parse import unquote

from bots.orbitonx.strings import URL_AUTH, URL_INIT, HEADERS, MSG_AUTH_ERROR, URL_INFO, URL_BALANCE, URL_QUESTS, \
    URL_STAKING_CLAIM, URL_TAP, MSG_STAKING_CLAIMED, MSG_STAKING_STARTED, MSG_STAKING_TAP, URL_TASKS, \
    MSG_TASK_CLAIMED, URL_TASK_CLAIM, URL_WATCH_AD, MSG_WATCHED_AD, URL_STOCKS, MSG_BALANCE


class BotFarmer(BaseFarmer):

    name = 'orbitonx_bot'
    upgrades = {}
    info = {}
    levels = {}
    quests = {}
    tasks = []
    next_claim = None
    app_extra = "friendId102796269"
    tokens = {}
    refreshable_token = True

    @property
    def initialization_data(self):
        return dict(peer=self.initiator.get_input_entity(self.name), 
                    app=InputBotAppShortName(self.initiator.get_input_entity(self.name), "orbitonx"),
                    start_param=self.app_extra)

    def set_headers(self, *args, **kwargs):
        self.headers = HEADERS.copy()
        self.get = api_response(super().get)
        self.post = api_response(super().post)
        self.delete = api_response(super().delete)
        self.patch = api_response(super().patch)

    def set_start_time(self):
        timestamps = (self.portfolio['finishStaking'], self.info['adNextAvailableTime'])
        self.start_time = min(map(to_localtz_timestamp, timestamps)) + 5

    def prepare_auth_data(self, url):
        from urllib.parse import unquote, parse_qsl
        parsed = parse_qsl(unquote(unquote(url)))
        user = json.loads(parsed[0][-1].split('user=')[-1])
        parsed.pop(0)
        parsed = dict(parsed)
        data = {
            "tgChatId": user['id'],
            "webAppInitData": {
                "user": user,
                "chat_instance": parsed['chat_instance'],
                "chat_type": parsed['chat_type'],
                "auth_date": parsed['auth_date'],
                "hash": parsed['hash']
            },
            "user": user
        }
        return data
        

    def authenticate(self, *args, **kwargs):
        auth_data = self.initiator.get_auth_data(**self.initialization_data)
        auth_data = self.prepare_auth_data(auth_data['url'])
        if response := self.post(URL_AUTH, json=auth_data):
            self.tokens = response['data']
            self.headers['Authorization'] = f"Bearer {self.tokens['token']}"
        else:
            self.is_alive = False
            raise Exception(MSG_AUTH_ERROR)

    def sync(self):
        if response := self.get(URL_INFO):
            self.info = response['data']

    def update_tasks(self):
        if response := self.get(URL_TASKS):
            self.tasks = response['data']['tasks']

    def check_tasks(self):
        self.update_tasks()
        for task in self.tasks:
            if task['status'] == 'not started':
                response = self.post(URL_TASKS, json={'taskId': task['id']})
                if response.get('status'):
                    if self.get(URL_TASK_CLAIM.format(**task)).get('status'):
                        self.log(MSG_TASK_CLAIMED.format(**task))
                        sleep(random() * 5)

    def watch_ad(self):
        while to_localtz_timestamp(self.info['adNextAvailableTime']) < time():
            if response := self.get(URL_WATCH_AD):
                if response['data']['balance'] > self.info['balance']:
                    self.info.update(response['data'])
                    self.log(MSG_WATCHED_AD)
                    sleep(random() * 20)
                else:
                    break


    def update_quests(self):
        if response := self.get(URL_QUESTS):
            self.quests.update(response['data'])

    @property
    def portfolio(self):
        return self.quests['quest']['portfolios'][0]

    def claim_or_farm(self):
        self.update_quests()
        # claim
        if self.portfolio['finishStaking'] and to_localtz_timestamp(self.portfolio['finishStaking']) < time() and not self.portfolio['active']:
            if response := self.patch(URL_STAKING_CLAIM, json={}):
                self.quests = response['data']
                self.log(MSG_STAKING_CLAIMED.format(**self.quests['quest']))
                self.update_quests()
        # tap
        if self.portfolio['active']:
            payload = dict(coins=[{'id': coin['id'], 'progress': 100} for coin in self.portfolio['coins']])
            payload['energy'] = 500
            response = self.patch(URL_TAP, json=payload)
            if response:
                self.log(MSG_STAKING_TAP)
                self.update_quests()
    
    def select_exchange(self):
        if not self.info['stoke']['id'] not in (8, 9):
            self.patch(URL_STOCKS, json={'stockId': 9})
            self.sync()

    @property
    def balance(self):
        return self.info['balance']

    def farm(self):
        self.sync()
        self.select_exchange()
        self.claim_or_farm()
        self.check_tasks()
        self.watch_ad()
        self.sync()
        self.log(MSG_BALANCE.format(balance=self.balance))

