import json
from random import randrange
from time import sleep, time
from bots.base.base import BaseFarmer
from bots.blum.strings import HEADERS, URL_REFRESH_TOKEN, URL_BALANCE, URL_TASKS, \
    URL_WEBAPP_INIT, URL_AUTH, URL_FARMING_CLAIM, URL_FARMING_START, URL_PLAY_START, \
    URL_PLAY_CLAIM,  URL_DAILY_REWARD, URL_FRIENDS_BALANCE, URL_FRIENDS_CLAIM, MSG_AUTH, \
    MSG_REFRESH, MSG_BALANCE, MSG_START_FARMING, MSG_CLAIM_FARM, MSG_BEGIN_GAME, \
    MSG_PLAYED_GAME, MSG_DAILY_REWARD, MSG_FRIENDS_CLAIM

GAME_RESULT_RANGE = (190, 280)
DEFAULT_EST_TIME = 60


class BotFarmer(BaseFarmer):

    name = "BlumCryptoBot"
    app_extra = "ref_ItXoLRFElL"
    initialization_data = dict(peer=name, bot=name, url=URL_WEBAPP_INIT)
    balance = None
    balance_data = None
    play_passes = None
    tasks = None
    auth_data = None
    refreshable_token = True

    def set_headers(self, *args, **kwargs):
        self.headers = HEADERS.copy()

    def set_start_time(self):
        if 'farming' in self.balance_data:
            est_time = (self.balance_data['farming']['endTime'] - self.balance_data['timestamp']) / 1000 + 1
            est_time = est_time if est_time > 0 else DEFAULT_EST_TIME
        else:
            est_time = DEFAULT_EST_TIME
        self.start_time = time() + est_time

    def authenticate(self):
        if not self.auth_data:
            self.log(MSG_AUTH)
            init_data = self.initiator.get_auth_data(**self.initialization_data)
            result = self.post(URL_AUTH, json={"query": init_data["authData"]})
            if result.status_code == 200:
                self.auth_data = result.json()['token']
                self.headers['Authorization'] = f"Bearer {self.auth_data['access']}"
    
    def refresh_token(self):
        self.log(MSG_REFRESH)
        self.headers.pop('Authorization')
        result = self.post(URL_REFRESH_TOKEN, json={"refresh": self.auth_data['refresh']})
        if result.status_code == 200:
            self.auth_data = result.json()
            self.headers['Authorization'] = f"Bearer {self.auth_data['access']}"

    
    def update_tasks(self):
        response = self.post(URL_TASKS)
        if response.status_code == 200:
            self.tasks = response.json()
    
    @property
    def estimate_time(self):
        if 'farming' in self.balance_data:
            est_time = (self.balance_data['farming']['endTime'] - self.balance_data['timestamp']) / 1000 + 1
            return est_time if est_time > 0 else DEFAULT_EST_TIME
        else:
            return DEFAULT_EST_TIME

    def update_balance(self):
        self.log(MSG_BALANCE)
        response = self.get(URL_BALANCE, headers=self.headers)
        if response.status_code == 200:
            self.balance_data = response.json()
            self.balance = self.balance_data['availableBalance']
            self.play_passes = self.balance_data['playPasses']
    
    def check_task(self):
        self.update_tasks()
        for task in self.tasks:
            if task['title'] == "Farm points" and task['status'] == "NOT_STARTED":
                self.start_farm()
    
    def start_farming(self):
        if 'farming' not in self.balance_data:
            self.log(MSG_START_FARMING)
            result = self.post(URL_FARMING_START)
            self.update_balance()
        elif self.balance_data["timestamp"] >= self.balance_data["farming"]["endTime"]:
            self.log(MSG_CLAIM_FARM.format(amount=self.balance_data["farming"]["balance"]))
            result = self.post(URL_FARMING_CLAIM)
            self.log(f"{result.status_code},  {result.text}")

    def play_game(self):
        for _ in range(self.play_passes or 0):
            self.log(MSG_BEGIN_GAME.format(self.play_passes))
            res = self.post(URL_PLAY_START)
            if res.status_code == 200:
                data = res.json()
                data['points'] = int(randrange(*GAME_RESULT_RANGE))
                sleep(23)
                while True:
                    result = self.post(URL_PLAY_CLAIM, json=data)
                    if result.status_code == 200:
                        break
                    else:
                        sleep(1)
                self.log(MSG_PLAYED_GAME.format(result=data['points']))
                self.update_balance()
    
    def daily_reward(self):
        result = self.get(URL_DAILY_REWARD)
        if result.status_code == 200:
            self.post(URL_DAILY_REWARD)
            {"ordinal":31,"reward":{"passes":7,"points":"70"}}
            msg_data = result.json()['days'][-1]
            self.log(MSG_DAILY_REWARD.format(days=msg_data['ordinal'],
                                             passes=msg_data['reward']['passes'],
                                             points=msg_data['reward']['points']))

    def friends_claim(self):
        friends_balance = self.get(URL_FRIENDS_BALANCE)
        if friends_balance.status_code == 200:
            if friends_balance.json().get('canClaim'):
                result = self.post(URL_FRIENDS_CLAIM)
                if result.status_code == 200:
                    self.log(MSG_FRIENDS_CLAIM.format(points=result.json()['claimBalance']))

    def farm(self):
        self.daily_reward()
        self.friends_claim()
        self.update_balance()
        self.play_game()
        self.start_farming()
