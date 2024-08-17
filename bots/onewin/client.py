import json
import re
from time import time as current_time, sleep
from random import choice, uniform, random
from bots.base.base import BaseFarmer
from telethon.types import InputBotAppShortName
from bots.onewin.strings import (
    HEADERS, BUILDING_INFO,
    URL_INIT, URL_ACCOUNT_BALANCE, URL_DAILY_REWARD_INFO, URL_MINING,
    URL_FRIENDS_INFO, URL_FRIEND_CLAIM,
    MSG_CURRENT_BALANCE, MSG_DAILY_REWARD, MSG_DAILY_REWARD_IS_COLLECTED,
    MSG_BUY_UPGRADE, MSG_BUY_BUILDING, MSG_ACCESS_TOKEN_ERROR, MSG_URL_ERROR,
    MSG_AUTHENTICATION_ERROR, MSG_ACCOUNT_INFO_ERROR, MSG_DAILY_REWARD_ERROR,
    MSG_INITIALIZATION_ERROR,MSG_FRIENDS_REWARD,MSG_FRIENDS_REWARD_ERROR
)
from bots.onewin.config import (
    FEATURES,UPGRADE_MAX_LEVEL
)


def sorted_by_payback(prepared):
    return sorted(prepared, key=lambda x: x['cost'] / x['profit'], reverse=False)


class BotFarmer(BaseFarmer):
    name = "token1win_bot"
    auth_data = None
    token = None
    extra_code = "refId6370423806"
    friends_coins = 0
    friends = 0

    @property
    def initialization_data(self):
        return dict(peer=self.name, 
                    app=InputBotAppShortName(self.initiator.get_input_entity(self.name), "start"),
                    start_param=self.extra_code)

    def authenticate(self):
        if not self.auth_data:
            try:
                init_data = self.initiator.get_auth_data(**self.initialization_data)
                self.auth_data = init_data
            except Exception as e:
                self.log(MSG_INITIALIZATION_ERROR.format(error=e))
        try:
            self.headers['x-user-id'] = str(self.auth_data['userId'])
            headers = self.headers.copy()
            response = self.post(URL_INIT, headers=headers, params=self.auth_data['authData'])
            if response.status_code == 200:
                result = response.json()
                if token := result.get("token"):
                    self.headers["Authorization"] = f"Bearer {token}"
                else:
                    self.error(MSG_ACCESS_TOKEN_ERROR)
            else:
                self.error(MSG_AUTHENTICATION_ERROR.format(status_code=response.status_code, text=response.text))
        except Exception as e:
            self.log(MSG_URL_ERROR.format(error=e))            

    def set_headers(self):
        self.headers = HEADERS.copy()

    def get_info(self, show=False):
        response = self.get(url=URL_ACCOUNT_BALANCE, headers=self.headers)
        if response.status_code == 200:
            result = response.json()
            self.balance = result.get("coinsBalance", 0)
            if show:
                self.log(MSG_CURRENT_BALANCE.format(coins=self.balance))
        else:
            self.error(MSG_ACCOUNT_INFO_ERROR.format(status_code=response.status_code,text=response.text))

    def daily_reward_info(self):
        response = self.get(URL_DAILY_REWARD_INFO, headers=self.headers)
        if response.status_code == 200:
            result = response.json()
            self.daily_reward_is_collected = result["days"][0]["isCollected"]

    def get_daily_reward(self):
        self.daily_reward_info()
        if self.daily_reward_is_collected == None:
            return None
        elif self.daily_reward_is_collected == False:
            response = self.post(url=URL_DAILY_REWARD_INFO, headers=self.headers)
            if response.status_code == 200:
                result = response.json()
                self.daily_reward = result["days"][0]["money"]
                self.log(MSG_DAILY_REWARD.format(coins=self.daily_reward))
            else:
                self.error(MSG_DAILY_REWARD_ERROR.format(status_code=response.status_code,text=response.text))
        else:
            self.log(MSG_DAILY_REWARD_IS_COLLECTED)

    def friends_info(self):
        response = self.get(URL_FRIENDS_INFO, headers=self.headers)
        if response.status_code == 200:
            result = response.json()
            self.friends = result.get("total_friends", 0)
            self.friends_coins = result.get("total_coins", 0)

    def friends_claim(self):
        self.friends_info()
        if self.friends_coins > 0:
            response = self.post(url=URL_FRIEND_CLAIM, headers=self.headers)
            if response.status_code == 200:
                result = response.json()
                coins_collected = result.get("coinsCollected", 0)
                self.log(MSG_FRIENDS_REWARD.format(coins=coins_collected))
            else:
                self.error(MSG_FRIENDS_REWARD_ERROR.format(status_code=response.status_code,text=response.text))

    def upgrades_list(self):
        response = self.get(URL_MINING, headers=self.headers)
        if response.status_code == 200:
            self.upgrades = response.json()

    def get_sorted_upgrades(self, sort_method):
        """
            1. Фильтруем карточки
                - доступные для покупки
                - с пассивным доходом
            2. Сортируем по профитности на каждую потраченную монету
        """
        methods = dict(payback=sorted_by_payback)
        prepared = []
        self.upgrades_list()
        for upgrade in self.upgrades:
            if (
                upgrade["profit"] > 0
                and upgrade["level"] <= UPGRADE_MAX_LEVEL - 1
                and upgrade["cost"] <= FEATURES["max_upgrade_cost"]
                and upgrade["cost"] / upgrade["profit"] <=  FEATURES["max_upgrade_payback"]
            ):
                upgrade["payback"] = round(upgrade["cost"] / upgrade["profit"],2)
                item = upgrade.copy()
                prepared.append(item)
        if prepared:
            sorted_items = [i for i in methods[sort_method](prepared)]
            return sorted_items
        return []

    def buy_upgrades(self):
        """ Покупаем лучшие апгрейды на всю котлету """
        if FEATURES["buy_upgrades"]:
            counter = 0
            num_purchases_per_cycle = FEATURES["num_purchases_per_cycle"]
            while True:
                if sorted_upgrades := self.get_sorted_upgrades(FEATURES["buy_decision_method"]):
                    upgrade = sorted_upgrades[0]
                    if upgrade["cost"]*2 <= self.balance \
                    and self.balance > FEATURES["min_cash_value_in_balance"] \
                    and num_purchases_per_cycle and counter < num_purchases_per_cycle:
                        self.upgrade(upgrade['id'])
                        sleep(2 + random() * 3)
                    else:
                        break
                else:
                    break

    def upgrade(self, upgrade_id, new_building=False):
        data = {"id": upgrade_id}
        english_name = re.sub(r'\d+', '', upgrade_id).lower()
        russian_name = BUILDING_INFO.get(english_name)["rus_name"]
        if new_building == False:
            match = re.search(r'\d+', data['id'])
            if match:
                current_level = int(match.group())
                upgrade_level = current_level + 1
                new_id = data['id'].replace(str(current_level), str(upgrade_level))
                data['id'] = new_id
                response = self.post(URL_MINING, json=data)
                if response.status_code == 200:
                    self.log(MSG_BUY_UPGRADE.format(name=russian_name, level=upgrade_level))
        else:
            response = self.post(URL_MINING, json=data)
            if response.status_code == 200:
                self.log(MSG_BUY_BUILDING.format(name=russian_name))
        self.get_info()

    def buy_new_buildings(self):
        my_buildings = {}
        for upgrade in self.upgrades:
            try:
                building_name = re.sub(r'\d+', '', upgrade["id"]).lower()
                building_level = upgrade["level"]
                my_buildings[building_name] = building_level
            except Exception as e:
                pass
        new_buildings = list(BUILDING_INFO.keys())
        self.get_info()
        for item in new_buildings:
            if not my_buildings.get(item):
                requirements = BUILDING_INFO[item]["requirements"]
                if (requirements == None) or (requirements["level"]<=my_buildings.get(requirements["name"],0)):
                    if BUILDING_INFO[item]["min_balance"] <= self.balance:
                        self.upgrade(BUILDING_INFO[item]["purchase_id"], new_building=True)

    def set_start_time(self):
        self.start_time = current_time() + uniform(FEATURES["minimum_delay"],FEATURES["maximum_delay"])

    def farm(self):
        self.authenticate()
        self.get_info(show=True)
        if FEATURES['get_daily_reward']:
            self.get_daily_reward()
        if FEATURES['friends_claim']:
            self.friends_claim()
        self.upgrades_list()
        if FEATURES['blind_upgrade']:
            self.buy_new_buildings()
        self.buy_upgrades()

