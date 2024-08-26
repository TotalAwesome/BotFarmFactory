"""
Author: Eyn
Date: 17-07-2024

"""
import json
import random
from time import time, sleep

from bots.base.base import BaseFarmer
from bots.tapcoins.config import BUY_UPGRADES, UPGRADES_COUNT, skip_ids, MIN_WAIT_TIME, MAX_WAIT_TIME
from bots.tapcoins.strings import HEADERS, URL_INIT, URL_LOGIN, URL_CARDS_CATEGORIES, URL_CARDS_LIST, \
    URL_CARDS_UPGRADE, URL_LUCKY_BOUNTY, MSG_NO_CARDS_TO_UPGRADE, \
    MSG_CARD_UPGRADED, MSG_NOT_ENOUGH_COINS, MSG_CARD_UPGRADED_COMBO, URL_DAILY, URL_DAILY_COMPLETE, \
    MSG_LOGIN_BONUS_COMPLETE, URL_USER_INFO, MSG_UPGRADING_CARDS, MSG_UPGRADE_COMPLETE, MSG_MAX_UPGRADES_REACHED, \
    URL_REFRESH, MSG_CURRENT_BALANCE, MSG_HOUR_EARNINGS, URL_GET_TASKS, URL_COMPLETE_TASK, MSG_TASK_COMPLETED

DEFAULT_EST_TIME = 60 * 10


class BotFarmer(BaseFarmer):
    name = "tapcoinsbot"
    token = None
    balance = None
    hours_earnings = None
    extra_code = 'ref_QjG2zG'
    refreshable_token = True
    codes_to_refresh = (401,)
    s = None
    initialization_data = dict(peer=name, bot=name, url=URL_INIT, start_param=extra_code)

    def set_headers(self, *args, **kwargs):
        self.headers = HEADERS.copy()

    def authenticate(self, *args, **kwargs):
        init_data = self.initiator.get_auth_data(**self.initialization_data)

        data = {
            'initData': init_data["authData"],
            'inviteCode': 'QjG2zG',
            'groupId': ''
        }

        result = self.post(URL_LOGIN, data=data)
        if result.status_code == 200:
            json_data = result.json()
            if 'data' in json_data and 'token' in json_data['data']:
                self.token = json_data['data']['token']
                self.is_alive = True
                self.s = json_data['data']['collect']['userInfo']['stock']
            else:
                self.is_alive = False

    def stock(self):
        stock = self.s
        self.log("Крутим рулетку")
        while stock > 0:
            data = {
                'lotteryId': '1',
                '_token': self.token,
            }
            response = self.post('https://xapi.tapcoins.app/lucky/lottery/draw', headers=self.headers, data=data)
            if response.status_code == 200:
                stock -= 1
                sleep(8)
            else:
                stock = 0
                self.log("Ошибка крутануть не вышло")
        data = {'_token': self.token, }
        response = self.post('https://xapi.tapcoins.app/user/assets/list', headers=self.headers, data=data).json()
        usdt = response['data'][0]['balance']
        self.log(f'Баланс USDT: {usdt}')

    def set_start_time(self):
        self.start_time = time() + random.uniform(MIN_WAIT_TIME, MAX_WAIT_TIME)

    def upgrade_cards(self):
        if BUY_UPGRADES:
            self.log(MSG_UPGRADING_CARDS)

            upgraded_cards = 0
            upgrades_count = UPGRADES_COUNT if UPGRADES_COUNT != 0 else 99999

            while True:
                if upgraded_cards >= upgrades_count:
                    self.log(MSG_MAX_UPGRADES_REACHED.format(limit=upgrades_count))
                    break

                cards = self.get_cards()
                if not cards:
                    self.log(MSG_NO_CARDS_TO_UPGRADE)
                    break

                cards = sorted(cards, key=lambda x: x['upgrade_earnings'] / x['upgrade_cost'], reverse=True)

                self.get_balance(False)

                upgraded = False

                for card in cards:
                    if self.balance >= card['upgrade_cost']:
                        self.post(URL_CARDS_UPGRADE, {'taskId': card['id'], '_token': self.token})
                        upgraded = True

                        level = card['current_level'] + 1

                        self.log(MSG_CARD_UPGRADED.format(name=card['name'], level=level, cost=card['upgrade_cost']))
                        upgraded_cards += 1

                        break

                if not upgraded:
                    self.log(MSG_NOT_ENOUGH_COINS)
                    break

            self.log(MSG_UPGRADE_COMPLETE)

    def get_cards(self):
        categories_response = self.post(URL_CARDS_CATEGORIES, data={'_token': self.token})
        categories_json = categories_response.json()

        cards = []

        for category in categories_json['data']:
            cards_response = self.post(URL_CARDS_LIST, {'categoryId': category['id'], '_token': self.token})
            cards_json = cards_response.json()

            for card in cards_json['data']:
                if card['upgradable']:
                    cards.append(card)
        return cards

    def get_bounty(self):
        data = {
            '_token': self.token
        }

        lucky_response = self.post(URL_LUCKY_BOUNTY, data=data)

        lucky_data = lucky_response.json()
        lucky_data_cards = lucky_data['data']['currents']
        lucky_sum = 0
        luckies = []

        for lucky in lucky_data_cards:
            if lucky['opened'] == 0:
                lucky_sum += lucky['lucky_coin']

                to_upgrade = {
                    'id': lucky['lucky_task_id'],
                }

                luckies.append(to_upgrade)

        cards = self.get_cards()
        cards_sum = 0
        cards_to_upgrade = []

        for card in cards:
            for lucky in luckies:
                if card['id'] == lucky['id']:
                    cards_sum += card['upgrade_cost']

                    cards_to_upgrade.append(card)
                    break

        if lucky_sum > cards_sum:
            self.upgrade_cards_by_id(cards_to_upgrade)

    def upgrade_cards_by_id(self, to_upgrade):
        for card in to_upgrade:
            self.get_balance(False)

            if self.balance >= card['upgrade_cost']:
                self.post(URL_CARDS_UPGRADE, {'taskId': card['id'], '_token': self.token})
                self.log(MSG_CARD_UPGRADED_COMBO.format(card['name']))

    def daily_bonus(self):
        data = {
            'type': 1,
            '_token': self.token
        }

        response = self.post(URL_DAILY, data=data)
        daily_login_json = response.json()
        for i, step in enumerate(daily_login_json['data']['steps']):
            if step['today'] and not step['claimed']:
                self.post(URL_DAILY_COMPLETE, data)

                self.log(MSG_LOGIN_BONUS_COMPLETE.format(step=i))
                break

    def get_hour_earnings(self, log=False):
        response = self.post(URL_USER_INFO, {'_token': self.token})
        data = response.json()['data']
        self.hours_earnings = data['hour_earnings']

        if log:
            self.log(MSG_HOUR_EARNINGS.format(earnings=self.hours_earnings))

    def get_balance(self, log=False):
        response = self.post(URL_USER_INFO, {'_token': self.token})
        data = response.json()['data']
        self.balance = data['balance']

        if log:
            self.log(MSG_CURRENT_BALANCE.format(balance=self.balance))

    def sync(self):
        return self.post(URL_REFRESH, {'_token': self.token})

    def refresh_token(self):
        self.initiator.connect()
        self.authenticate()
        self.initiator.disconnect()

    def complete_tasks(self):
        response = self.post(URL_GET_TASKS, {'adv': 0, '_token': self.token})
        tasks = response.json()['data']
        for task in tasks:
            if task['completed'] == 0 and task['verifiable'] == 0:
                sleep(1)
                if task['id'] not in skip_ids:
                    i = task['id']
                    t = task['title']
                    self.post(URL_COMPLETE_TASK, {'adv': 0, 'taskId': task['id'], '_token': self.token})
                    self.log(f'Выполнили таску: {i} {t}')
        sleep(2)
        response = self.post(URL_GET_TASKS, {'adv': 1, '_token': self.token})
        tasks = response.json()['data']
        for task in tasks:
            if task['completed'] == 0 and task['verifiable'] == 0:
                count = task['daily_completion_count']
                if task['completed'] == 0 and task['verifiable'] == 0 and count < 5:
                    sleep(2)
                    i = task['id']
                    t = task['title']
                    self.post(URL_COMPLETE_TASK, {'adv': 1, 'taskId': task['id'], '_token': self.token})
                    self.log(f'Выполнили таску: {i} {t}')

    def farm(self):
        self.sync()
        self.get_balance(True)
        self.stock()
        self.get_hour_earnings(True)
        self.daily_bonus()
        self.get_bounty()
        self.complete_tasks()
        self.upgrade_cards()
        self.get_hour_earnings(True)
