from time import sleep, time
from random import random, shuffle
from bots.base.base import BaseFarmer
from bots.base.utils import to_localtz_timestamp, api_response
from bots.solstone.strings import HEADERS, URL_AUTH, URL_TASKS, URL_CLAIM_TASK, URL_INIT, URL_CLAIM_FARMED, \
    URL_START_FARM, MSG_CLAIM_FARMED, MSG_FARMING_STARTED, MSG_TASK_CLAIMED, URL_REFS_INFO, URL_CLAIM_REFS, \
    MSG_CLAIM_REFS
from .utils import utc_timestamp


class BotFarmer(BaseFarmer):
    name = "solstonebot"
    extra_code = "102796269"
    initialization_data = dict(peer=name, bot=name, url=URL_INIT)
    base_payload = None
    time_shift = (8 * 60 * 60 + 10) * 1000

    def timestamp(self):
        return int(utc_timestamp() * 1000)

    def set_headers(self, *args, **kwargs):
        self.headers = HEADERS.copy()
        self.get = api_response(super().get)
        self.post = api_response(super().post)
        self.delete = api_response(super().delete)

    def authenticate(self, *args, **kwargs):
        auth_data = self.initiator.get_auth_data(**self.initialization_data)["authData"]
        self.base_payload = {'initData': auth_data, 'project': 'SolStone'}
        self.info = self.post(URL_AUTH, json=self.base_payload)

    def get_tasks(self):
        return self.get(URL_TASKS)

    def claim_tasks(self):
        if not (tasks := self.get_tasks()):
            return
        shuffle(tasks)
        for task in tasks:
            if task['id'] not in self.info['completed_quest_ids']:
                payload = self.base_payload.copy()
                payload.update(questId=task['id'])
                self.post(URL_CLAIM_TASK, json=payload)
                self.info['completed_quest_ids'].append(task['id'])
                self.log(MSG_TASK_CLAIMED.format(amount=task['points_reward']))
                sleep(random() * 10)

    def claim_or_start_farming(self):
        farming_started = int(self.info['farm_started_at']) if self.info.get('farm_started_at') else None
        if farming_started and self.timestamp() > farming_started + self.time_shift:
            self.debug(f"{farming_started=} {self.timestamp()} {self.time_shift + farming_started=}")
            farming_started = None
            response = self.post(URL_CLAIM_FARMED, json=self.base_payload, return_codes=(400,))
            if response:
                self.log(MSG_CLAIM_FARMED)
                self.info.update(response)
        if not farming_started:
            payload = self.base_payload.copy()
            payload['startedAt'] = self.timestamp()
            farm_response = self.post(URL_START_FARM, json=payload)
            if farm_response:
                self.log(MSG_FARMING_STARTED)
                self.info['farm_started_at'] = farm_response['started_at']

    def set_start_time(self):
        self.start_time = (int(self.info.get('farm_started_at')) + self.time_shift) / 1000

    def claim_refs(self):
        if response := self.get(URL_REFS_INFO.format(**self.info)):
            total_farmed = sum(int(ref['points']) for ref in response)
            if total_farmed - int(self.info.get('ref_points_claimed', 0)):
                response = self.post(URL_CLAIM_REFS, json=self.base_payload)
                if response:
                    self.info['ref_points_claimed'] = int(self.info.get('ref_points_claimed', 0)) + response['claimed_points']
                    self.log(MSG_CLAIM_REFS.format(amount=response['claimed_points']))


    def farm(self):
        self.claim_tasks()
        self.claim_or_start_farming()
        self.claim_refs()
        