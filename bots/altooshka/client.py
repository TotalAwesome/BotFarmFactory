from time import sleep, time

from bots.altooshka.strings import HEADERS, URL_INIT, URL_LOGIN, URL_GIRLS_ACTION, MSG_ACTION_COMPLETE, \
    MSG_ACTION_IS_NOT_AVAILABLE, MSG_ACTION_UNDRESS_COMPLETE, URL_FOLLOW, URL_X_CHALLENGE, MSG_CURRENT_BALANCE
from bots.base.base import BaseFarmer

DEFAULT_EST_TIME = 60 * 10


class BotFarmer(BaseFarmer):
    name = "altooshka_bot"
    balance = None
    girls = None
    auth_data = None
    end_time = None
    extra_code = 'z6HfRqEhax4'
    initialization_data = dict(peer=name, bot=name, url=URL_INIT, start_param=extra_code)

    def set_headers(self, *args, **kwargs):
        self.headers = HEADERS.copy()

    def authenticate(self, *args, **kwargs):
        init_data = self.initiator.get_auth_data(**self.initialization_data)

        self.auth_data = init_data['authData']

        login_url = URL_LOGIN + '?' + self.auth_data + '&ref_code=z6HfRqEhax4'

        result = self.get(login_url, return_codes=(404,))

        if result.status_code == 201:
            json_data = result.json()

            if json_data['status'] == 'success' and json_data['success']:
                user_data = json_data['data']['user']

                self.balance = user_data['gems']

                self.girls = user_data['girls']

                self.is_alive = True
        else:
            self.initiator.join_group('https://t.me/AltOOshka_EN')
            self.initiator.subscribe_channel('https://t.me/altooshka_ton')
            result = self.get(URL_FOLLOW + '?' + self.auth_data)

            json = result.json()
            if json['success'] and json['data']['isFollowed']:
                result = self.post(login_url, return_codes=(404,))
                json = result.json()

                if json['success']:
                    user_data = json['data']['user']

                    self.balance = user_data['gems']
                    self.girls = user_data['girls']

                    self.log(MSG_CURRENT_BALANCE.format(balance=self.balance))

                    self.do_x_challenge()

                    self.is_alive = True

    def set_start_time(self):
        if self.end_time:
            self.start_time = self.end_time
        else:
            est_time = DEFAULT_EST_TIME
            self.start_time = time() + est_time

    def set_end_time(self, action_end_time):
        if self.end_time is None or action_end_time < self.end_time:
            self.end_time = action_end_time

    def process_girls(self):
        updated_data = self.update_girls_actions(self.girls)

        for girl_id, girl_data in updated_data.items():
            actions = girl_data.get('actions', {})
            action_ids = list(actions.keys())

            for action_id in action_ids[:3]:
                action_end_time = actions[action_id]
                if action_end_time < time():
                    self.process_action(girl_id, action_id, action_end_time)

            if len(action_ids) >= 7:
                action_id = action_ids[6]
                action_end_time = actions[action_id]
                if action_end_time < time():
                    self.process_action(girl_id, action_id, action_end_time)

            for action_id in action_ids[3:6]:
                action_end_time = actions[action_id]
                if action_end_time < time():
                    self.process_action(girl_id, action_id, action_end_time)

    def process_action(self, girl_id, action_id, action_end_time):
        if action_end_time > time():
            self.set_end_time(action_end_time)
            return

        sleep(5)
        payload = {"girl_id": girl_id, "action_id": action_id}
        url = URL_GIRLS_ACTION + '?' + self.auth_data

        response = self.post(url, json=payload, return_codes=(403,))
        response_json = response.json()

        if response_json['success']:

            self.balance = response_json['data']['gems']
            self.set_end_time(response_json['data']['availableAt'])

            reward = response_json['data']['gemsChange']
            if reward > 0:
                self.log(MSG_ACTION_COMPLETE.format(action=action_id, girl=girl_id, reward=reward))
            else:
                self.log(MSG_ACTION_UNDRESS_COMPLETE.format(girl=girl_id, reward=reward))

        else:
            self.log(MSG_ACTION_IS_NOT_AVAILABLE.format(action=action_id, girl=girl_id))

    def farm(self):
        self.show_balance()
        self.process_girls()

    @staticmethod
    def update_girls_actions(data):

        for key, girl in data.items():
            existing_actions = girl.get("actions", {})
            start_index = (int(key) - 1) * 7 + 1

            for i in range(7):
                action_id = str(start_index + i)
                if action_id not in existing_actions:
                    existing_actions[action_id] = 0

            girl["actions"] = existing_actions

        return data

    def do_x_challenge(self):
        payload = {"actionName": "x_com_channel_subscribe"}
        url = URL_X_CHALLENGE + '?' + self.auth_data

        self.post(url, json=payload, return_codes=(403, 404))

    def show_balance(self):
        self.log(MSG_CURRENT_BALANCE.format(balance=self.balance))
