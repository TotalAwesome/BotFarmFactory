import json
from random import randint, uniform
from time import sleep, time
from bots.base.base import BaseFarmer
from bots.dotcoin.strings import (
    HEADERS, URL_INIT, URL_GET_USER_INFO, URL_GET_TOKEN, 
    URL_TRY_YOUR_LUCK, URL_SAVE_COINS, URL_ADD_MULTITAP, URL_ADD_ATTEMPT,
    MSG_AUTH, API_KEY, MSG_BALANCE, MSG_LEVEL, 
    MSG_ENERGY, MSG_LIMIT_ENERGY, MSG_MULTITAP_LEVEL, 
    MSG_BONUS_RECEIVED, MSG_BONUS_ALREADY_RECEIVED, 
    MSG_BONUS_NOT_RECEIVED, MSG_GAME_PLAYED, MSG_GAME_NOT_PLAYED,
    MSG_BOOST_SUCCESS, MSG_BOOST_ALREADY_MAX, MSG_BOOST_FAILED, BOOST_NAMES
)
from bots.dotcoin.config import COINS, MAX_CLICK_LVL, MAX_LIMIT_LVL

class BotFarmer(BaseFarmer):
    name = "dotcoin_bot"
    initialization_data = dict(peer=name, bot=name, url=URL_INIT)
    info = {}
    extra_code = "r_762252877"
    auth_data = None

    def set_headers(self, token=None):
        self.headers = HEADERS.copy()
        if token:
            self.headers['Authorization'] = f'Bearer {token}'
            self.headers['apikey'] = API_KEY
        else:
            self.headers['Authorization'] = f'Bearer {API_KEY}'
        self.headers['x-extra-code'] = self.extra_code

    def authenticate(self):
        if not self.auth_data:
            self.log(MSG_AUTH)
            init_data = self.initiator.get_auth_data(**self.initialization_data)
            payload = {
                "initData": init_data["authData"]
            }
            self.set_headers()  # Устанавливаем заголовки с API_KEY
            result = self.post(URL_GET_TOKEN, headers=self.headers, json=payload)
            if result.status_code == 200:
                token_data = result.json()
                if token := token_data.get("token"):
                    self.auth_data = token
                    self.set_headers(self.auth_data)  # Обновляем заголовки с полученным токеном
                else:
                    self.error("Не удалось получить access token")
            else:
                self.error(f"Ошибка аутентификации. Код состояния: {result.status_code}, Ответ: {result.text}")

    def fetch_account_info(self, log_info=True):
        result = self.post(URL_GET_USER_INFO, headers=self.headers, json={})
        if result.status_code == 200:
            info = result.json()
            if log_info:
                self.log(f"Уровень: {info['level']}")
                self.log(f"Баланс: {info['balance']:,}")
                self.log(f"Энергия: {info['daily_attempts']}")
                self.log(f"Мультитап: {info['multiple_clicks']}")
                self.log(f"Лимит энергии: {info['limit_attempts'] - 9}")
            return info
        else:
            self.error(f"Не удалось получить информацию об аккаунте. Код состояния: {result.status_code}, Ответ: {result.text}")
            return None

    def claim_bonus(self):
        result = self.post(URL_TRY_YOUR_LUCK, headers=self.headers, json={"coins": 150000})
        if result.status_code == 200:
            response_data = result.json()
            if response_data.get('success', False):
                self.log(MSG_BONUS_RECEIVED)
            else:
                self.log(MSG_BONUS_ALREADY_RECEIVED)
        else:
            self.error(f"{MSG_BONUS_NOT_RECEIVED}. Код состояния: {result.status_code}, Ответ: {result.text}")

    def play_game(self, remaining_energy):
        coins = randint(COINS[0], COINS[1])
        result = self.post(URL_SAVE_COINS, headers=self.headers, json={"coins": coins})
        if result.status_code == 200:
            response_data = result.json()
            if response_data.get('success', False):
                self.log(f"{MSG_GAME_PLAYED.format(coins=coins)}, Оставшаяся энергия: {remaining_energy}")
            else:
                self.log(MSG_GAME_NOT_PLAYED)
        else:
            self.error(f"{MSG_GAME_NOT_PLAYED}. Код состояния: {result.status_code}, Ответ: {result.text}")

    def upgrade_boost(self, boost_type, current_level, max_level):
        url = URL_ADD_MULTITAP if boost_type == 'Click_LVL' else URL_ADD_ATTEMPT
        data = {"lvl": current_level}
        if current_level >= max_level:
            self.log(MSG_BOOST_ALREADY_MAX.format(boost_name=BOOST_NAMES[boost_type]))
            return False
        result = self.post(url, headers=self.headers, json=data)
        if result.status_code == 200:
            response_data = result.json()
            if response_data.get('success', False):
                self.log(MSG_BOOST_SUCCESS.format(boost_name=BOOST_NAMES[boost_type]))
                return True
            else:
                self.log(MSG_BOOST_FAILED.format(boost_name=BOOST_NAMES[boost_type]))
                return False
        else:
            self.error(f"{MSG_BOOST_FAILED.format(boost_name=BOOST_NAMES[boost_type])}. Код состояния: {result.status_code}, Ответ: {result.text}")
            return False

    def farm(self):
        self.authenticate()
        info = self.fetch_account_info()
        if not info:
            return

        self.claim_bonus()
        games_available = info['daily_attempts']

        # Прокачка бустов
        if self.upgrade_boost('Click_LVL', info['multiple_clicks'], MAX_CLICK_LVL):
            # Обновляем информацию после успешной прокачки
            info = self.fetch_account_info(log_info=False)

        if self.upgrade_boost('Limit_LVL', info['limit_attempts'] - 9, MAX_LIMIT_LVL):
            # Обновляем информацию после успешной прокачки
            info = self.fetch_account_info(log_info=False)

        if games_available > 0:
            self.log(f"Игр доступно: {games_available}")
            while games_available > 0:
                self.play_game(games_available - 1)
                games_available -= 1
                sleep(randint(12, 23))

            # Обновляем и выводим только баланс после всех игр
            info = self.fetch_account_info(log_info=False)
            self.log(f"Баланс: {info['balance']:,}")

    def set_start_time(self):
        # Устанавливаем следующий заход через случайное время от 3 до 6 часов
        self.start_time = time() + uniform(3 * 60 * 60, 6 * 60 * 60)
