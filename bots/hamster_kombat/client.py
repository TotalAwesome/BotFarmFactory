import re

from datetime import datetime
from bots.base.base import BaseFarmer
from base64 import b64decode
from time import time, sleep
from random import randrange, choice, random, uniform
from threading import Thread
from telethon.types import InputBotAppShortName
from bots.hamster_kombat.promo import PromoGenerator
from bots.hamster_kombat.strings import URL_BOOSTS_FOR_BUY, URL_BUY_BOOST, URL_BUY_UPGRADE, \
    URL_SYNC, URL_TAP, URL_UPGRADES_FOR_BUY, HEADERS, BOOST_ENERGY, URL_CHECK_TASK, \
    URL_CLAIM_DAILY_COMBO, MSG_BUY_UPGRADE, MSG_COMBO_EARNED, MSG_TAP, MSG_CLAIMED_COMBO_CARDS, \
    MSG_SYNC, URL_CONFIG, URL_CLAIM_DAILY_CIPHER, MSG_CIPHER, URL_INIT, URL_AUTH, URL_SELECT_EXCHANGE, \
    URL_LIST_TASKS, MSG_TASK_COMPLETED, MSG_TASK_NOT_COMPLETED, URL_GET_SKINS, URL_BUY_SKIN, \
    MSG_BOOST, MSG_BOOST_AVAILABLE, MSG_TAP_SIM, \
    PROMO_TOKENS, MSG_BUY_SKIN, MSG_PROMO_COMPLETED, \
    URL_APPLY_PROMO, URL_GET_PROMOS, \
    MSG_PROMO_UPDATE_ERROR, MSG_PROMO_OK, MSG_PROMO_ERROR, MSG_TRY_PROMO, MSG_PROMO_STATUS
from bots.hamster_kombat.config import FEATURES
from bots.hamster_kombat.utils import sorted_by_payback, sorted_by_price, sorted_by_profit, sorted_by_profitness, \
    get_keys_count_per_game
    

def generate_promo_keys(dict_with_keys, **kwargs):
    client = PromoGenerator(**kwargs)
    while True:
        new_key = client.get_promo()
        actual = dict_with_keys['actual']
        activated = dict_with_keys['activated']
        actual[client.promo_id] = actual.get(client.promo_id, [])
        activated[client.promo_id] = activated.get(client.promo_id, [])
        if not new_key in actual[client.promo_id] \
            and not new_key in activated[client.promo_id]:
            actual[client.promo_id].append(new_key)
        sleep(5)


class BotFarmer(BaseFarmer):

    name = 'hamster_kombat_bot'
    app_extra = 'kentId102796269'
    state = None
    boosts = None
    upgrades = None
    task_checked_at = None
    config_version = None
    promo_status = {}
    promo_threads = {}
    promo_keys = {'actual': {},
                  'activated': {}}
    skins_info = []
    my_skins_ids = []

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
        self.start_promo_collector()

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

    @property
    def promo_completed(self):
        return all([game['keys_per_day'] == game['keys_today'] 
                    for game in self.promo_status.values()])

    def start_promo_collector(self):
        for promo_id, app_token in PROMO_TOKENS.items():
            if not promo_id in BotFarmer.promo_threads:
                kwargs = dict(promo_id=promo_id, 
                              app_token=app_token, 
                              proxies=self.proxies, 
                              dict_with_keys=BotFarmer.promo_keys)
                thread = Thread(target=generate_promo_keys, kwargs=kwargs)
                BotFarmer.promo_threads[promo_id] = thread
                thread.start()

    def set_exchange(self):
        self.sync()
        if not self.exchage_id:
            eid = choice(('binance', 'okx', 'bybit', 'gate_io', 'bingx'))
            self.post(URL_SELECT_EXCHANGE, json={'exchangeId': eid})

    def set_start_time(self):
        """
        Берём минимальное из значений:
        - рандомного значения между минимальным и максимальным периодом до следующего захода
        - (если включены тапы) периода накопления энергии
        - (если включены промокоды и на сегодня введены не все) случайное значение от 10 до 15 минут
        """
        sleep_seconds = []
        minimum_farm_sleep = FEATURES.get("minimum_farm_sleep", 2 * 60 * 60)
        maximum_farm_sleep = FEATURES.get("maximum_farm_sleep", 3 * 60 * 60)
        bot_farm_sleep = uniform(minimum_farm_sleep, maximum_farm_sleep)
        sleep_seconds.append(bot_farm_sleep)
        if FEATURES.get('taps', True):
            tap_sleep_seconds = int(self.state['maxTaps'] / self.state['tapsRecoverPerSec'])            
            sleep_seconds.append(tap_sleep_seconds)
        if FEATURES.get('apply_promo', True) and not self.promo_completed:
            promo_next_step = choice(range(10 * 60, 15 * 60))
            sleep_seconds.append(promo_next_step)
        self.start_time = time() + min(sleep_seconds)

    def get_cipher_data(self):
        result = self.post(URL_CONFIG).json()
        return result['dailyCipher']

    def claim_daily_cipher(self):
        """ Разгадываем морзянку """
        cipher_data = self.get_cipher_data()
        if not cipher_data['isClaimed']:
            raw_cipher = cipher_data['cipher'][:3] + cipher_data['cipher'][4:]
            cipher = b64decode(raw_cipher).decode()
            self.log(MSG_CIPHER.format(cipher=cipher))
            self.post(URL_CLAIM_DAILY_CIPHER, json={"cipher": cipher})

    def get_skins_info(self):
        """ Получаем данные о скинах в игре """
        response = self.get(f"{URL_CONFIG}/{self.config_version}")
        if response.status_code == 200:
            result = response.json()
            self.skins_info = result.get('config', {}).get('skins')

    def get_skins_state(self):
        """ Получаем данные о купленных скинах """
        my_skins = self.state.get('skin', {}).get('available')
        self.my_skins_ids = [item['skinId'] for item in my_skins]

    def buy_skins(self):
        self.get_skins_info()
        self.get_skins_state()
        max_skin_price = FEATURES.get('max_skin_price', 0)
        for skin in self.skins_info:
            skin_condition = {}
            if skin.get('condition', {}).get('_type') == 'UserLevel':
                skin_condition['user_level'] = skin.get('condition', {}).get('level')
            skin_price = skin.get('price')
            skin_id = skin.get('id')
            if (
                skin_price <= self.balance
                and skin_condition.get('user_level', 0) <= self.level
                and skin_price <= max_skin_price
                and skin_id not in self.my_skins_ids
                and (not skin.get('expiresAt') or datetime.utcnow() < datetime.fromisoformat(skin['expiresAt'][:-1]))
                ):
                response = self.buy_skin(skin_id)
                result = response.json()
                if response.status_code == 200:
                    self.log(MSG_BUY_SKIN.format(skin_name=skin_id))
                    self.sync()
                    sleep(2 + random()*5)
                else:
                    break

    def buy_skin(self, skin_name):
        data = {"skinId": skin_name, "timestamp": int(time())}
        return self.post(URL_BUY_SKIN, json=data)

    def sync(self):
        self.log(MSG_SYNC)
        try:
            response = self.post(url=URL_SYNC)
            self.state = response.json()["clickerUser"]
            self.config_version = response.headers.get('config-version')
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
        self.log(MSG_BOOST.format(boostype = boost_name))

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
                and FEATURES.get('apply_boosts', True)
            ):
                self.log(MSG_BOOST_AVAILABLE.format(boostid = boost["id"]))
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
                and (not FEATURES['max_upgrade_payback'] or \
                    upgrade["price"] / upgrade["profitPerHourDelta"] <= FEATURES['max_upgrade_payback'])
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
            reward = task.get('rewardCoins', 0)
            is_completed = task['isCompleted']

            if not task_id.startswith('hamster_youtube'):
                continue

            if not is_completed:
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

    def update_promos(self):
        response = self.post(URL_GET_PROMOS)
        if response.status_code == 200:
            result = response.json()
            self.promo_status = {}
            states = result.get('states', [])
            activated_keys = get_keys_count_per_game(states)
            for game in result.get('promos', []):
                self.promo_status[game['promoId']] = {
                    "keys_per_day": game['keysPerDay'],
                    "game_name": game['title']['en'],
                    "keys_today": activated_keys.get(game['promoId'], 0),
                }
        else:
            self.log(MSG_PROMO_UPDATE_ERROR)
            self.promo_status = None

    def apply_promo(self):
        self.update_promos()
        for promo_id, promo_state in self.promo_status.items():
            if promo_state['keys_per_day'] == (keys_today := promo_state['keys_today']):
                continue
            promo_keys = BotFarmer.promo_keys
            actual = promo_keys['actual'][promo_id] = promo_keys['actual'].get(promo_id, [])
            activated = promo_keys['activated'][promo_id] = promo_keys['activated'].get(promo_id, [])
            if actual:
                promo_code = actual.pop(0)
                data = {"promoCode": promo_code}
                self.log(MSG_TRY_PROMO.format(code=promo_code))
                response = self.post(URL_APPLY_PROMO, json=data)
                if response.status_code == 200:
                    result = response.json()
                    self.promo_status[promo_id]['keys_today'] = result.get('promoState', {}).get('receiveKeysToday', keys_today)
                    self.log(MSG_PROMO_OK)
                else:
                    self.log(MSG_PROMO_ERROR)
                if activated:
                    activated.pop(0)
                activated.append(promo_code)

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
            self.claim_combo_reward()
        if FEATURES.get('buy_skins', True):
            self.buy_skins()        
        if FEATURES.get('apply_promo', True):
            self.apply_promo()
        if self.is_taps_boost_available:
            self.boost(BOOST_ENERGY)
            self.sync()
            tap_sim_sec = choice(range(FEATURES.get('tap_wait'[0], 110), FEATURES.get('tap_wait'[1], 130)))
            self.log(MSG_TAP_SIM.format(sec = tap_sim_sec))
            sleep(tap_sim_sec)
            self.tap()

        self.log(" ".join(f"{k}: {v} |" for k, v in self.stats.items()))