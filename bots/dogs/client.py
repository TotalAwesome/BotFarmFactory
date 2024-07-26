"""
Author: Eyn
Date: 24-07-2024

"""
from random import randrange
from time import time, sleep

from bots.base.base import BaseFarmer
from bots.dogs.strings import HEADERS, URL_INIT, URL_LOGIN, MSG_CURRENT_BALANCE, \
    MSG_CURRENT_FRIENDS, URL_FRIENDS, MSG_LOGIN_ERROR, URL_GET_TASKS, URL_VERIFY_TASK, MSG_TASK_COMPLETE, \
    MSG_TASK_ERROR

DEFAULT_EST_TIME = 60 * 10
LOGIN_RANGE = (100, 1300)


class BotFarmer(BaseFarmer):
    name = "dogshouse_bot"
    balance = None
    user_id = None
    ref_code = None
    auth_data = None
    extra_code = '07wokQJZTrS5FSrah8SigQ'
    initialization_data = dict(peer=name, bot=name, url=URL_INIT, start_param=extra_code)

    def set_headers(self, *args, **kwargs):
        self.headers = HEADERS.copy()

    def authenticate(self, *args, **kwargs):
        try:

            init_data = self.initiator.get_auth_data(**self.initialization_data)
            self.auth_data = init_data['authData']
            login_url = URL_LOGIN + '?' + 'invite_hash=' + self.extra_code

            result = self.post(login_url, data=self.auth_data)

            if result.status_code == 200:
                self.handle_successful_login(result.json())
        except Exception as e:
            self.log(MSG_LOGIN_ERROR.format(e=e))
            self.is_alive = False

    def handle_successful_login(self, json_data):
        user_data = json_data
        self.balance = user_data['balance']
        self.ref_code = user_data['reference']
        self.user_id = user_data['telegram_id']
        self.is_alive = True

    def set_start_time(self):
        max_time = 23 * 3600
        random_time = randrange(DEFAULT_EST_TIME, max_time)
        self.start_time = time() + random_time

    def farm(self):
        self.show_balance()
        self.show_friends()
        self.process_tasks()

    def show_balance(self):
        self.log(MSG_CURRENT_BALANCE.format(balance=self.balance))

    def show_friends(self):
        url = URL_FRIENDS + f'?user_id={self.user_id}&reference={self.ref_code}'
        response = self.get(url)
        response_json = response.json()
        self.log(MSG_CURRENT_FRIENDS.format(total=response_json['count']))

    def process_tasks(self):
        response = self.get(URL_GET_TASKS.format(user_id=self.user_id, reference=self.ref_code)).json()

        for task in response:
            if not task['complete']:
                sleep(randrange(4, 7))
                self.process_task(task)

    def process_task(self, task):
        try:
            response = self.post(
                URL_VERIFY_TASK.format(slug=task['slug'], user_id=self.user_id, reference=self.ref_code)).json()
            if response['success']:
                self.log(MSG_TASK_COMPLETE.format(slug=task['slug'], reward=task['reward']))
            else:
                self.log(MSG_TASK_ERROR.format(slug=task['slug']))
        except Exception as e:
            self.log(MSG_TASK_ERROR.format(slug=task['slug']))
