from time import sleep, time
from bots.altooshka.strings import HEADERS, URL_INIT, URL_LOGIN, URL_GIRLS_ACTION, MSG_ACTION_COMPLETE, \
    MSG_ACTION_IS_NOT_AVAILABLE, MSG_ACTION_UNDRESS_COMPLETE, URL_FOLLOW, URL_X_CHALLENGE, MSG_CURRENT_BALANCE, \
    URL_TG_CHAT, URL_TG_GROUP
from bots.base.base import BaseFarmer

DEFAULT_EST_TIME = 60 * 10
SLEEP_DURATION = 5
ACTION_COUNT = 7
EARLY_ACTIONS = 3
FOLLOW_ACTION_INDEX = 6


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
        login_url = URL_LOGIN + '?' + self.auth_data + '&ref_code=' + self.extra_code

        result = self.get(login_url, return_codes=(404,))

        if result.status_code == 201:
            self.handle_successful_login(result.json())
        else:
            self.handle_failed_login(login_url)

    def handle_successful_login(self, json_data):
        if json_data['status'] == 'success' and json_data['success']:
            user_data = json_data['data']['user']
            self.balance = user_data['gems']
            self.girls = user_data['girls']
            self.is_alive = True

    def handle_failed_login(self, login_url):
        self.initiator.join_group(URL_TG_CHAT)
        self.initiator.subscribe_channel(URL_TG_GROUP)
        result = self.get(URL_FOLLOW + '?' + self.auth_data)
        json = result.json()
        if json['success'] and json['data']['isFollowed']:
            result = self.post(login_url, return_codes=(404,))
            json = result.json()
            if json['success']:
                self.handle_successful_login(json)
                self.log(MSG_CURRENT_BALANCE.format(balance=self.balance))
                self.do_x_challenge()
                self.is_alive = True

    def set_start_time(self):
        self.start_time = self.end_time if self.end_time else time() + DEFAULT_EST_TIME

    def set_end_time(self, action_end_time):
        if self.end_time is None or action_end_time < self.end_time:
            self.end_time = action_end_time

    def process_girls(self):
        self.update_girls_actions(self.girls)
        for girl_id, girl_data in self.girls.items():
            actions = girl_data.get('actions', {})
            action_ids = list(actions.keys())

            self.process_first_actions(girl_id, actions, action_ids)
            self.process_follow_action(girl_id, actions, action_ids)
            self.process_remaining_actions(girl_id, actions, action_ids)

    def process_first_actions(self, girl_id, actions, action_ids):
        if len(action_ids) < ACTION_COUNT or actions[action_ids[FOLLOW_ACTION_INDEX]] <= time():
            for action_id in action_ids[:EARLY_ACTIONS]:
                self.try_process_action(girl_id, action_id, actions[action_id])

    def process_follow_action(self, girl_id, actions, action_ids):
        if len(action_ids) >= ACTION_COUNT:
            self.try_process_action(girl_id, action_ids[FOLLOW_ACTION_INDEX], actions[action_ids[FOLLOW_ACTION_INDEX]])

    def process_remaining_actions(self, girl_id, actions, action_ids):
        for action_id in action_ids[EARLY_ACTIONS:FOLLOW_ACTION_INDEX]:
            self.try_process_action(girl_id, action_id, actions[action_id])

    def try_process_action(self, girl_id, action_id, action_end_time):
        if action_end_time < time():
            self.process_action(girl_id, action_id, action_end_time)

    def process_action(self, girl_id, action_id, action_end_time):
        if action_end_time > time():
            self.set_end_time(action_end_time)
            return

        sleep(SLEEP_DURATION)
        payload = {"girl_id": girl_id, "action_id": action_id}
        url = URL_GIRLS_ACTION + '?' + self.auth_data

        response = self.post(url, json=payload, return_codes=(403,))
        response_json = response.json()

        if response_json['success']:
            self.handle_successful_action(response_json, girl_id, action_id)
        else:
            self.log(MSG_ACTION_IS_NOT_AVAILABLE.format(action=action_id, girl=girl_id))

    def handle_successful_action(self, response_json, girl_id, action_id):
        self.balance = response_json['data']['gems']
        self.set_end_time(response_json['data']['availableAt'])

        reward = response_json['data']['gemsChange']
        if reward > 0:
            self.log(MSG_ACTION_COMPLETE.format(action=action_id, girl=girl_id, reward=reward))
        else:
            self.log(MSG_ACTION_UNDRESS_COMPLETE.format(girl=girl_id, reward=reward))

    def farm(self):
        self.show_balance()
        self.process_girls()

    def update_girls_actions(self, data):
        min_timestamp = float('inf')

        for key, girl in data.items():
            existing_actions = girl.get("actions", {})
            start_index = (int(key) - 1) * ACTION_COUNT + 1

            for i in range(ACTION_COUNT):
                action_id = str(start_index + i)
                if action_id not in existing_actions:
                    existing_actions[action_id] = 0

            girl["actions"] = existing_actions

            for action_id, timestamp in existing_actions.items():
                if time() < timestamp < min_timestamp:
                    min_timestamp = timestamp

        self.end_time = min_timestamp if min_timestamp != float('inf') else None

    def do_x_challenge(self):
        payload = {"actionName": "x_com_channel_subscribe"}
        url = URL_X_CHALLENGE + '?' + self.auth_data
        self.post(url, json=payload, return_codes=(403, 404))

    def show_balance(self):
        self.log(MSG_CURRENT_BALANCE.format(balance=self.balance))
