"""
Author: Eyn
Date: 18-07-2024

"""
from time import sleep, time

from bots.base.base import BaseFarmer
from bots.hexn.strings import HEADERS, URL_INIT, URL_LOGIN, MSG_FARMING_ALREADY_STARTED, MSG_FARMING_ERROR, URL_CLAIM, \
    MSG_CLAIMED, \
    MSG_CURRENT_BALANCE, URL_START_FARMING, MSG_FARMING_STARTED, MSG_QUEST_COMPLETED, MSG_QUEST_ERROR, \
    MSG_QUEST_STARTING_ERROR, URL_QUEST_START, URL_QUEST_CLAIM

DEFAULT_EST_TIME = 60 * 10


class BotFarmer(BaseFarmer):
    name = "hexn_bot"
    codes_to_refresh = (401,)
    refreshable_token = True
    user_data = None
    auth_data = None
    balance = None
    end_time = None
    farming_data = None
    referral = 'tgWebAppStartParam=63b093b0-fcb8-41b5-8f50-bc61983ef4e3'
    initialization_data = dict(peer=name, bot=name, url=URL_INIT, start_param=referral)

    def set_headers(self, *args, **kwargs):
        self.headers = HEADERS.copy()

    def authenticate(self, *args, **kwargs):
        init_data = self.initiator.get_auth_data(**self.initialization_data)

        self.auth_data = init_data['authData']
        data = {
            'init_data': init_data['authData']
        }
        try:
            result = self.post(URL_LOGIN, json=data)

            if result.status_code == 200:
                json_data = result.json()
                if json_data['status'] == 'OK':
                    self.user_data = user_data = json_data['data']
                    self.balance = user_data.get('balance')
                    self.is_alive = True
        except Exception as e:
            self.is_alive = False
            self.log(str(e), error=True)

    def set_start_time(self):
        if self.end_time:
            self.start_time = self.end_time
        else:
            est_time = DEFAULT_EST_TIME
            self.start_time = time() + est_time

    def check_farming_status(self):

        farming_status = self.user_data.get('farming', {})

        if not farming_status:
            self.start_farming()

        if farming_status.get('end_at', 0) // 1000 > time():
            self.log(MSG_FARMING_ALREADY_STARTED)
            self.end_time = farming_status.get('end_at', 0) // 1000

            return
        else:
            self.claim()

    def start_farming(self):

        data = {
            'init_data': self.auth_data,
        }

        result = self.post(URL_START_FARMING, json=data)
        response_json = result.json()

        if response_json.get('status') == 'OK':
            self.log(MSG_FARMING_STARTED)

        self.get_state()

        farming_status = self.user_data.get('farming', {})
        self.end_time = farming_status.get('end_at', 0) // 1000

    def claim(self):
        data = {
            'init_data': self.auth_data,
        }

        result = self.post(URL_CLAIM, json=data)
        response_json = result.json()

        if response_json.get('status') == 'OK':
            self.log(MSG_CLAIMED)

            self.start_farming()
        else:
            self.log(MSG_FARMING_ERROR)

    def farm(self):
        self.show_balance()
        self.check_farming_status()
        self.quests()
        self.show_balance()

    def get_state(self):
        data = {
            'init_data': self.auth_data
        }
        try:
            result = self.post(URL_LOGIN, json=data)

            if result.status_code == 200:
                json_data = result.json()
                if json_data['status'] == 'OK':
                    self.user_data = user_data = json_data['data']
                    self.balance = user_data.get('balance')
        except Exception as e:
            self.log(str(e), error=True)

    def show_balance(self):
        self.get_state()
        self.log(MSG_CURRENT_BALANCE.format(balance=self.balance))

    def quests(self):
        executed_quests = self.user_data.get('executed_quests', {})

        for quest_id, quest in self.user_data['config']['quests'].items():
            if str(quest_id) not in executed_quests:
                quest_name = quest.get('description', 'Unnamed Quest')
                quest_points = quest.get('points_amount', 'Unknown amount')

                data = {
                    'init_data': self.auth_data,
                    'quest_id': int(quest_id)
                }
                try:
                    self.post(URL_QUEST_START, json=data)
                except Exception as e:
                    self.log(MSG_QUEST_STARTING_ERROR.format(quest_name=quest_name))

                    continue

                sleep(5)

                result = self.post(URL_QUEST_CLAIM, json=data)
                response_json = result.json()

                if response_json.get('status') == 'OK':

                    self.log(MSG_QUEST_COMPLETED.format(quest_name=quest_name, quest_points=quest_points))
                else:
                    self.log(MSG_QUEST_ERROR.format(quest_name=quest_name))
