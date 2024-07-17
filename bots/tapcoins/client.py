from time import time

from bots.base.base import BaseFarmer
from bots.tapcoins.strings import HEADERS, URL_INIT, URL_LOGIN, URL_COLLECT, URL_CARDS_CATEGORIES, URL_CARDS_LIST, \
    MSG_CURRENT_BALANCE, URL_CARDS_UPGRADE, URL_LUCKY_BOUNTY, MSG_NO_CARDS_TO_UPGRADE, MSG_SORTING_CARDS, \
    MSG_CARD_UPGRADED, MSG_NOT_ENOUGH_COINS, MSG_CARD_UPGRADED_COMBO, URL_DAILY, URL_DAILY_COMPLETE, \
    MSG_LOGIN_BONUS_COMPLETE

DEFAULT_EST_TIME = 60


class BotFarmer(BaseFarmer):
    name = "tapcoinsbot"
    token = None
    balance = None
    # extra_code = 'ref_QjG2zG'
    initialization_data = dict(peer=name, bot=name, url=URL_INIT)

    def set_headers(self, *args, **kwargs):
        self.headers = HEADERS.copy()

    def authenticate(self, *args, **kwargs):
        init_data = self.initiator.get_auth_data(**self.initialization_data)

        data = {
            'initData': init_data["authData"],
            'inviteCode': '',
            'groupId': ''
        }

        result = self.post(URL_LOGIN, data=data)
        if result.status_code == 200:
            json_data = result.json()
            if 'data' in json_data and 'token' in json_data['data']:
                self.token = json_data['data']['token']
                self.is_alive = True
            else:
                self.is_alive = False

    def set_start_time(self):
        est_time = DEFAULT_EST_TIME
        self.start_time = time() + est_time

    def get_balance(self):
        data = {
            'coin': 0,
            'power': 1500,
            'turbo': 0,
            '_token': self.token
        }

        response = self.post(URL_COLLECT, data=data)
        json = response.json()
        self.balance = json['data']['userInfo']['coin']

        self.log(MSG_CURRENT_BALANCE.format(result=self.balance))

    def upgrade_cards(self):
        while True:
            cards = self.get_cards()
            if not cards:
                self.log(MSG_NO_CARDS_TO_UPGRADE)
                break

            self.log(MSG_SORTING_CARDS)

            cards = sorted(cards, key=lambda x: x['upgrade_earnings'] / x['upgrade_cost'], reverse=True)

            self.get_balance()

            upgraded = False

            for card in cards:
                if self.balance >= card['upgrade_cost']:
                    self.post(URL_CARDS_UPGRADE, {'taskId': card['id'], '_token': self.token})
                    upgraded = True

                    self.log(MSG_CARD_UPGRADED.format(card['name']))
                    break

            if not upgraded:
                self.log(MSG_NOT_ENOUGH_COINS)
                break

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
            self.get_balance()

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

    def farm(self):
        self.get_balance()
        self.daily_bonus()
        self.get_bounty()
        self.upgrade_cards()
