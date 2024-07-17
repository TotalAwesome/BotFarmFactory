import random
from time import time

from bots.base.base import BaseFarmer
from bots.tapcoins.config import BUY_UPGRADES, UPGRADES_COUNT
from bots.tapcoins.strings import HEADERS, URL_INIT, URL_LOGIN, URL_CARDS_CATEGORIES, URL_CARDS_LIST, \
    URL_CARDS_UPGRADE, URL_LUCKY_BOUNTY, MSG_NO_CARDS_TO_UPGRADE, \
    MSG_CARD_UPGRADED, MSG_NOT_ENOUGH_COINS, MSG_CARD_UPGRADED_COMBO, URL_DAILY, URL_DAILY_COMPLETE, \
    MSG_LOGIN_BONUS_COMPLETE, URL_USER_INFO, MSG_UPGRADING_CARDS, MSG_UPGRADE_COMPLETE, MSG_MAX_UPGRADES_REACHED, \
    URL_REFRESH

DEFAULT_EST_TIME = 60 * 10


class BotFarmer(BaseFarmer):
    name = "tapcoinsbot"
    token = None
    balance = None
    hours_earnings = None
    extra_code = 'ref_QjG2zG'
    refreshable_token = True
    codes_to_refresh = (401,)
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
            else:
                self.is_alive = False

    def set_start_time(self):
        if BUY_UPGRADES:
            try:
                cards = self.get_cards()
                if not cards:
                    self.log(MSG_NO_CARDS_TO_UPGRADE)
                    return

                cards = sorted(cards, key=lambda x: x['upgrade_earnings'] / x['upgrade_cost'], reverse=True)

                self.get_balance()
                self.get_hour_earnings()

                earnings_per_second = round(self.hours_earnings / 3600)

                first_card = cards[0]
                time_to_upgrade = round(first_card['upgrade_cost'] / earnings_per_second) + random.randint(60, 120)

                self.start_time = time() + time_to_upgrade
            except Exception as e:
                est_time = DEFAULT_EST_TIME
                self.start_time = time() + est_time
        else:
            est_time = DEFAULT_EST_TIME
            self.start_time = time() + est_time

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

                self.get_balance()

                upgraded = False

                for card in cards:
                    if self.balance >= card['upgrade_cost']:
                        self.post(URL_CARDS_UPGRADE, {'taskId': card['id'], '_token': self.token})
                        upgraded = True

                        self.log(MSG_CARD_UPGRADED.format(card['name']))
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

    def get_hour_earnings(self):
        response = self.post(URL_USER_INFO, {'_token': self.token})
        data = response.json()['data']
        self.hours_earnings = data['hour_earnings']

    def get_balance(self):
        response = self.post(URL_USER_INFO, {'_token': self.token})
        data = response.json()['data']
        self.balance = data['balance']

    def sync(self):
        return self.post(URL_REFRESH, {'_token': self.token})
    
    def refresh_token(self):
        self.initiator.connect()
        self.authenticate()
        self.initiator.disconnect()

    def farm(self):
        self.sync()
        self.get_balance()
        self.daily_bonus()
        self.get_bounty()
        self.upgrade_cards()
