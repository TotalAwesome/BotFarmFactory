"""
(c) TotalAwesome
"""

import uuid
import time
import string
from random import randint, choices, choice
from requests import Session

from bots.base.strings import USER_AGENTS
from bots.hamster_kombat.strings import (
    GET_PROMO_HEADERS, 
    URL_REGISTER_EVENT, URL_LOGIN, URL_CREATE_CODE
    )

def generate_random_client_id():
    current_time = int(time.time() * 1000)
    random_part = randint(100, 999)
    random_first = int(str(current_time)[:10] + str(random_part))
    random_seconds = ''.join(choices(string.digits, k=19))
    return f"{random_first}-{random_seconds}"


def get_event_data(game_id):
    return {"promoId": game_id,
            "eventId": f"{uuid.uuid1()}",
            "eventOrigin": "undefined"}

def retry(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                result = func(*args, **kwargs)
                if result.status_code == 200:
                    return result
                elif result.status_code == 429:
                    time.sleep(30)
                else:
                    time.sleep(1)
            except Exception as e:
                time.sleep(5)
    return wrapper
            


class PromoGenerator(Session):


    def __init__(self, app_token, promo_id, proxies) -> None:
        self.request = retry(self.request)
        super().__init__()
        self.headers = GET_PROMO_HEADERS
        self.app_token = app_token
        self.promo_id = promo_id
        self.proxies = proxies
        self.headers = {}
        self.headers['User-Agent'] = choice(USER_AGENTS)
        self.authenticate()

    def authenticate(self):
        payload = {"appToken": self.app_token,
                   "clientId": generate_random_client_id(),
                   "clientOrigin": "deviceid"}
        response = self.post(URL_LOGIN, json=payload, proxies=self.proxies)
        if response.status_code == 200:
            token = response.json()['clientToken']
            self.headers['Authorization'] = 'Bearer ' + response.json()['clientToken']
            return
        raise Exception('Can\'t log in')
    
    def get_promo(self):
        while True:
            self.post(URL_REGISTER_EVENT, json=get_event_data(game_id=self.promo_id), proxies=self.proxies)
            data = {"promoId": self.promo_id}
            response = self.post(URL_CREATE_CODE, json=data, proxies=self.proxies)
            if response.status_code == 200 and (promo := response.json().get('promoCode', '')):
                return promo
            time.sleep(1)
 

if __name__ == '__main__':
    wizard = PromoGenerator()
    print(wizard.get_promo())
