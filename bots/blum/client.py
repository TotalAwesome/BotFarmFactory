import json
from random import randrange, choice, random
from time import sleep, time
from telethon.types import InputBotAppShortName
from bots.base.base import BaseFarmer
from bots.blum.strings import HEADERS, URL_REFRESH_TOKEN, URL_BALANCE, URL_TASKS, \
    URL_WEBAPP_INIT, URL_AUTH, URL_FARMING_CLAIM, URL_FARMING_START, URL_PLAY_START, \
    URL_PLAY_CLAIM,  URL_DAILY_REWARD, URL_FRIENDS_BALANCE, URL_FRIENDS_CLAIM, MSG_AUTH, \
    MSG_REFRESH, MSG_BALANCE, MSG_START_FARMING, MSG_CLAIM_FARM, MSG_BEGIN_GAME, MSG_GAME_OFF, \
    MSG_PLAYED_GAME, MSG_DAILY_REWARD, MSG_FRIENDS_CLAIM, URL_CHECK_NAME, MSG_INPUT_USERNAME, \
    URL_TASK_CLAIM, URL_TASK_START, MSG_TASK_CLAIMED, MSG_TASK_STARTED
from bots.blum.config import MANUAL_USERNAME, GAME_TOGGLE_ON

GAME_RESULT_RANGE = (190, 280)
DEFAULT_EST_TIME = 60


class BotFarmer(BaseFarmer):

    name = "BlumCryptoBot"
    app_extra = "ref_ItXoLRFElL"
    balance = None
    balance_data = None
    play_passes = None
    tasks = None
    auth_data = None
    codes_to_refresh = (401,)
    refreshable_token = True

    @property
    def initialization_data(self):
        return dict(peer=self.name, 
                    app=InputBotAppShortName(self.initiator.get_input_entity(self.name), "app"),
                    start_param=self.app_extra)

    def check_name(self, username):
        response = self.post(URL_CHECK_NAME, json={'username': username}, return_codes=(400, 409))
        return response.status_code == 200

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
                self.auth_data = result.json().get('token')
                if not self.auth_data:
                    if not self.create_account_and_get_token(init_data=init_data["authData"]):
                        return
                self.headers['Authorization'] = f"Bearer {self.auth_data['access']}"
    
    def create_account_and_get_token(self, init_data):
        if not MANUAL_USERNAME:
            import string
            charmap = string.ascii_letters + '_'
        while True:
            if not MANUAL_USERNAME:
                username = ''.join(str(choice(charmap)) for _ in range(randrange(6, 12)))
            else:
                username = input(MSG_INPUT_USERNAME)
            if self.check_name(username=username):
                payload = dict(query=init_data,
                               referralToken=self.app_extra.split('_')[-1],
                               username=username)
                result = self.post(URL_AUTH, json=payload)
            else:
                continue
            if result.status_code == 200:
                self.auth_data = result.json().get('token')
                if not self.auth_data:
                    self.error("Blum не зарегистрирован по реф. ссылке")
                    self.is_alive = False
                    return
                return True
            sleep(5)


    def refresh_token(self):
        self.log(MSG_REFRESH)
        self.headers.pop('Authorization')
        result = self.post(URL_REFRESH_TOKEN, json={"refresh": self.auth_data['refresh']})
        if result.status_code == 200:
            self.auth_data = result.json()
            self.headers['Authorization'] = f"Bearer {self.auth_data['access']}"

    
    def update_tasks(self):
        response = self.get(URL_TASKS)
        if response.status_code == 200:
            result = response.json()
            self.tasks = []
            for item in result:
                if task_group := item["tasks"]:
                    self.tasks = self.tasks + task_group
    
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
    
    def check_tasks(self):
        self.update_tasks()
        for task in self.tasks:
            if task['type'] == 'SOCIAL_SUBSCRIPTION' and task['status'] == "NOT_STARTED":
                response = self.post(URL_TASK_START.format(**task))
                if response.status_code == 200:
                    self.log(MSG_TASK_STARTED.format(**task))
                    task.update(response.json())
                    sleep(random() * 5)
            if task['status'] == "READY_FOR_CLAIM":
                response = self.post(URL_TASK_CLAIM.format(**task))
                if response.status_code == 200:
                    self.log(MSG_TASK_CLAIMED.format(**task))
                    task.update(response.json())
                    sleep(random() * 5)
    
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
        if not GAME_TOGGLE_ON:
            self.log(MSG_GAME_OFF)
            return
        else: 
            for _ in range(self.play_passes or 0):
                self.log(MSG_BEGIN_GAME.format(self.play_passes))
                res = self.post(URL_PLAY_START)
                if res.status_code == 200:
                    data = res.json()
                    data['points'] = int(randrange(*GAME_RESULT_RANGE))
                    sleep(30)
                    while True:
                        result = self.post(URL_PLAY_CLAIM, json=data)
                        if result.status_code == 200:
                            break
                        else:
                            sleep(1)
                    self.log(MSG_PLAYED_GAME.format(result=data['points']))
                    self.update_balance()
    
    def daily_reward(self):
        result = self.get(URL_DAILY_REWARD, return_codes=(404,))
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
        self.check_tasks()
