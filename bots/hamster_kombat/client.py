import re

from bots.base.base import BaseFarmer
from base64 import b64decode
from time import time, sleep
from random import randrange, choice, random, uniform
from telethon.types import InputBotAppShortName
from bots.hamster_kombat.strings import URL_BOOSTS_FOR_BUY, URL_BUY_BOOST, URL_BUY_UPGRADE, \
    URL_SYNC, URL_TAP, URL_UPGRADES_FOR_BUY, HEADERS, BOOST_ENERGY, URL_CHECK_TASK, \
    URL_CLAIM_DAILY_COMBO, MSG_BUY_UPGRADE, MSG_COMBO_EARNED, MSG_TAP, MSG_CLAIMED_COMBO_CARDS, \
    MSG_SYNC, URL_CONFIG, URL_CLAIM_DAILY_CIPHER, MSG_CIPHER, URL_INIT, URL_AUTH, URL_SELECT_EXCHANGE, \
    URL_LIST_TASKS, MSG_TASK_COMPLETED, MSG_TASK_NOT_COMPLETED, URL_GET_SKINS, URL_BUY_SKIN, \
    DICT_SKINS, MSG_BUY_SKIN, MSG_SKIN_NOT_ENOUGH_MONEY, MSG_SKIN_ALREADY_PURCHASED
from bots.hamster_kombat.config import FEATURES
from bots.hamster_kombat.utils import sorted_by_payback, sorted_by_price, sorted_by_profit, sorted_by_profitness
    

class BotFarmer(BaseFarmer):

    name = 'hamster_kombat_bot'
    app_extra = 'kentId102796269'
    # initialization_data = dict(peer=name, bot=name, url=URL_INIT, start_param=extra_code)
    state = None
    boosts = None
    upgrades = None
    task_checked_at = None

    @property
    def exchage_id(self):
        return self.state.get('exchangeId')

    @property
    def initialization_data(self):
        return dict(peer=self.name, 
                    app=InputBotAppShortName(self.initiator.get_input_entity(self.name), "start"),
                    start_param=self.app_extra)

    def set_headers(self):
        self.headers = HEADERS.copy()

    def authenticate(self):
        init_data = self.initiator.get_auth_data(**self.initialization_data)
        result = self.post(URL_AUTH, json={"initDataRaw": init_data["authData"]})
        if result.status_code == 200:
            if token := result.json().get('authToken'):
                self.headers['Authorization'] = f"Bearer {token}"
                self.set_exchange()
                return
        self.is_alive = False
        raise KeyError

    def set_exchange(self):
        self.sync()
        if not self.exchage_id:
            eid = choice(('binance', 'okx', 'bybit', 'gate_io', 'bingx'))
            self.post(URL_SELECT_EXCHANGE, json={'exchangeId': eid})


    def set_start_time(self):
        tap_sleep_seconds = int(self.state['maxTaps'] / self.state['tapsRecoverPerSec'])
        minimum_farm_sleep = FEATURES.get("minimum_farm_sleep",2*60*60)
        maximum_farm_sleep = FEATURES.get("maximum_farm_sleep",3*60*60)
        bot_farm_sleep = uniform(minimum_farm_sleep, maximum_farm_sleep) + random()
        sleep_seconds = max(tap_sleep_seconds, bot_farm_sleep)
        self.start_time = time() + sleep_seconds

    def get_cipher_data(self):
        result = self.post(URL_CONFIG).json()
        return result['dailyCipher']

    def claim_daily_cipher(self):
        """
        Разгадываем морзянку
        """
        cipher_data = self.get_cipher_data()
        if not cipher_data['isClaimed']:
            raw_cipher = cipher_data['cipher']
            re_result = re.search('\d+', raw_cipher[3:])
            if re_result:
                str_len = re_result[0]
                raw_cipher = raw_cipher.replace(str_len, "", 1)
                raw_cipher = raw_cipher.encode()
                cipher = b64decode(raw_cipher).decode()
                self.log(MSG_CIPHER.format(cipher=cipher))
                self.post(URL_CLAIM_DAILY_CIPHER, json={"cipher": cipher})

    def get_skins(self):
        response = self.post(URL_GET_SKINS)
        if response.status_code == 200:
            result = response.json()
            if result := result.get("skins"):
                skins_info = {}
                skins_info["featured"] = list(filter(lambda x: x['isFeatured'], result))
                skins_info["available"] = list(filter(lambda x: x['isAvailable'], result))
                return skins_info
            else:
                return None
        else:
            return None

    def buy_skins(self):
        skins_info = self.get_skins()
        if not skins_info:
            return
        available_skins = skins_info.get("available")
        for available_skin in available_skins:
            skin_id = available_skin.get("id")
            if skin_id in DICT_SKINS:
                skin_cost = DICT_SKINS[skin_id]
                if self.balance > skin_cost:
                    response = self.buy_skin(skin_id)
                    result = response.json()
                    if response.status_code == 200:
                        self.log(MSG_BUY_SKIN.format(skin_name=skin_id))
                        self.sync()
                        sleep(random()*5)
                    elif response.status_code == 400 and result.get("error_code") == "INSUFFICIENT_FUNDS":
                        self.log(MSG_SKIN_NOT_ENOUGH_MONEY)
                        break
                    elif response.status_code == 400 and result.get("error_code") == "SKIN_ALREADY_AVAILABLE":
                        self.log(MSG_SKIN_ALREADY_PURCHASED)
                        sleep(2 + random()*5)
                        continue
                    else:
                        break


    def sync(self):
        self.log(MSG_SYNC)
        try:
            response = self.post(url=URL_SYNC)
            self.state = response.json()["clickerUser"]
        except Exception as e:
            pass

    def daily_reward(self):
        """ Получение ежедневной награды """
        data = {"taskId":"streak_days"}
        if not self.task_checked_at or time() - self.task_checked_at >= 60 * 60:
            self.post(URL_CHECK_TASK, json=data)
            self.task_checked_at = time()
        
    def tap(self):
        taps_count = self.available_taps or self.recover_per_sec
        data = {"count": taps_count,
                "availableTaps": self.available_taps - taps_count,
                "timestamp": int(time())}
        self.post(URL_TAP, json=data).json()
        self.log(MSG_TAP.format(taps_count=taps_count))

    def boost(self, boost_name=BOOST_ENERGY):
        data = {"boostId": boost_name, "timestamp": int(time())}
        self.post(URL_BUY_BOOST, json=data)

    def upgrade(self, upgrade_name):
        data = {"upgradeId": upgrade_name, "timestamp": int(time())}
        return self.post(URL_BUY_UPGRADE, json=data)

    def upgrdades_list(self):
        self.upgrades = self.post(URL_UPGRADES_FOR_BUY).json()

    def boosts_list(self):
        self.boosts = self.post(URL_BOOSTS_FOR_BUY).json()

    @property
    def balance(self):
        if self.state:
            return self.state["balanceCoins"]

    @property
    def level(self):
        if self.state:
            return self.state["level"]

    @property
    def available_taps(self):
        if self.state:
            return self.state["availableTaps"]

    @property
    def recover_per_sec(self):
        if self.state:
            return self.state["tapsRecoverPerSec"]

    @property
    def is_taps_boost_available(self):
        self.boosts_list()
        if not self.boosts:
            return
        for boost in self.boosts["boostsForBuy"]:
            if (
                boost["id"] == BOOST_ENERGY
                and boost["cooldownSeconds"] == 0
                and boost["level"] <= boost["maxLevel"]
            ):
                return True
    

    def get_sorted_upgrades(self, method):
        """
            1. Фильтруем карточки 
                - доступные для покупки
                - не просроченные
                - с пассивным доходом
                - без ожидания перезарядки
            2. Сортируем по профитности на каждую потраченную монету
        """
        methods = dict(payback=sorted_by_payback, 
                       price=sorted_by_price,
                       profit=sorted_by_profit,
                       profitness=sorted_by_profitness)
        prepared = []
        for upgrade in self.upgrades.get("upgradesForBuy"):
            if (
                upgrade["isAvailable"]
                and not upgrade["isExpired"]
                and upgrade["profitPerHourDelta"] > 0
                and not upgrade.get("cooldownSeconds")
                and upgrade["price"] / upgrade["profitPerHourDelta"] <= FEATURES['max_upgrade_payback']
            ):
                item = upgrade.copy()
                if 'condition' in item :
                    item.pop('condition')
                prepared.append(item)
        if prepared:
            sorted_items = [i for i in methods[method](prepared)] # if i['price'] <= self.balance]
            return sorted_items
        return []

    def buy_upgrades(self, method):
        """ Покупаем лучшие апгрейды на всю котлету """
        while True:
            self.upgrdades_list()
            if sorted_upgrades := self.get_sorted_upgrades(method):
                upgrade = sorted_upgrades[0]
                if upgrade['price'] <= self.balance:
                    result = self.upgrade(upgrade['id'])
                    if result.status_code == 200:
                        self.state = result.json()["clickerUser"]
                    self.log(MSG_BUY_UPGRADE.format(**upgrade))
                    minimum_upgrade_delay = FEATURES.get("minimum_upgrade_delay", 5)
                    maximum_upgrade_delay = FEATURES.get("maximum_upgrade_delay", 10)
                    sleep(uniform(minimum_upgrade_delay, maximum_upgrade_delay) + random())
                else:
                    break
            else:
                break

    def claim_combo_reward(self):
        """ Если вдруг насобирал комбо - нужно получить награду """
        combo = self.upgrades.get('dailyCombo', {})
        upgrades =  combo.get('upgradeIds', [])
        combo_cards = " ".join(upgrades)
        self.log(MSG_CLAIMED_COMBO_CARDS.format(cards=combo_cards))
        if combo and len(upgrades) == 3:
            if combo.get('isClaimed') is False:
                result = self.post(URL_CLAIM_DAILY_COMBO)
                if result.status_code == 200:
                    self.state = result.json()["clickerUser"]
                    self.log(MSG_COMBO_EARNED.format(coins=combo['bonusCoins']))

    def update_tasks(self):
        response = self.post(URL_LIST_TASKS)
        if response.status_code == 200:
            result = response.json()
            self.tasks = list(filter(lambda d: d['isCompleted'] != True, result["tasks"]))   

    def make_tasks(self):
        self.update_tasks()
        for task in self.tasks:
            task_id = task['id']
            reward = task['rewardCoins']
            is_completed = task['isCompleted']

            if not task_id.startswith('hamster_youtube'):
                continue

            if reward > 0:
                sleep(random() + choice(range(5, 10)))
                data = {'taskId': task_id}
                response = self.post(URL_CHECK_TASK, json=data)
                if response.status_code == 200:
                    result = response.json()
                    result = result["task"]
                    is_completed = result.get('isCompleted')
                    if is_completed:
                        self.log(MSG_TASK_COMPLETED.format(reward=reward))
                    else:
                        self.log(MSG_TASK_NOT_COMPLETED)

    @property
    def stats(self):
        return {
            "уровень" : self.level,
            "энергия" : self.available_taps,
            'баланс' : round(self.balance, 0),
            "доход в час" : round(self.state['earnPassivePerHour'], 0)
        }
    
    @property
    def log_prefix(self):
        return f"[{self.name}]\t "

    def farm(self):
        self.sync()
        self.claim_daily_cipher()
        if FEATURES.get('taps', True):
            self.tap()
        self.daily_reward()
        self.make_tasks()
        if FEATURES.get('buy_upgrades', True):
            self.buy_upgrades(FEATURES.get('buy_decision_method', 'payback'))
        if FEATURES.get('buy_skins', True):
            self.buy_skins()
        self.claim_combo_reward()
        if self.is_taps_boost_available:
            self.boost(BOOST_ENERGY)
        self.log(" ".join(f"{k}: {v} |" for k, v in self.stats.items()))
        # sleep(choice(range(1, 10)))
        # sleep(FEATURES.get('delay_between_attempts', 60 * 10))