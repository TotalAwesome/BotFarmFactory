import json
import re
from time import time as current_time, sleep
from random import choice, uniform
from bots.base.base import BaseFarmer
from bots.onewin.strings import (
    HEADERS, BUILDING_INFO,
    URL_INIT,URL_ACCOUNT_BALANCE,URL_DAILY_REWARD_INFO,URL_MINING,
    MSG_CURRENT_BALANCE,MSG_DAILY_REWARD,MSG_DAILY_REWARD_IS_COLLECTED,
    MSG_BUY_UPGRADE,MSG_BUY_BUILDING
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
    initialization_data = dict(peer=name, bot=name, url=URL_INIT)

    def authenticate(self):
        if not self.auth_data:
            init_data = self.initiator.get_auth_data(**self.initialization_data)
            self.auth_data = {
                "initData": init_data["authData"]
            }

    def set_headers(self):
        self.headers = HEADERS.copy()
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"
        self.headers["x-extra-code"] = self.extra_code

    def get_token(self):
        self.set_headers()
        auth_data = self.auth_data["initData"]
        try:
            result = self.post(URL_INIT, headers=self.headers,params=auth_data)
            if result.status_code == 200:
                token_data = result.json()
                if token := token_data.get("token"):
                    self.token = token
                    self.set_headers()
                else:
                    self.error("Не удалось получить access token")
            else:
                self.error(f"Ошибка аутентификации. Код состояния: {result.status_code}, Ответ: {result.text}")
        except Exception as e:
            self.log(f"Ошибка при разборе URL для аутентификации: {e}")

    def get_info(self, show=False):
        response = self.get(url=URL_ACCOUNT_BALANCE, headers=self.headers)
        if response.status_code == 200:
            result = response.json()
            self.balance = result.get("coinsBalance", 0)
            if show:
                self.log(MSG_CURRENT_BALANCE.format(coins=self.balance))
        else:
            result = "POST ERROR {status_code}{text}".format(status_code=response.status_code,text=response.text)
        return result

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
                result = "POST ERROR {status_code}{text}".format(status_code=response.status_code,text=response.text)
            return result
        else:
            self.log(MSG_DAILY_REWARD_IS_COLLECTED)

    def upgrades_list(self):
        response = self.get(URL_MINING, headers=self.headers)
        if response.status_code == 200:
            self.upgrades = response.json()
            # print(json.dumps(self.upgrades, indent=4))

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
            if my_buildings.get(item) == None:
                requirements = BUILDING_INFO[item]["requirements"]
                if (requirements == None) or (requirements["level"]<=my_buildings.get(requirements["name"],0)):
                    if BUILDING_INFO[item]["min_balance"] <= self.balance:
                        self.upgrade(BUILDING_INFO[item]["purchase_id"], new_building=True)

    def set_start_time(self):
        self.start_time = current_time() + uniform(FEATURES["minimum_delay"],FEATURES["maximum_delay"])

    def farm(self):
        self.authenticate()
        self.get_token()
        self.get_info(show=True)
        if FEATURES['get_daily_reward']:
            self.get_daily_reward()
        self.upgrades_list()
        if FEATURES['blind_upgrade']:
            self.buy_new_buildings()
        self.buy_upgrades()

