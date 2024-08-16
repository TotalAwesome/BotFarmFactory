import uuid
import time
import string
from random import randint, choices
from requests import Session

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


class PromoGenerator(Session):

    def __init__(self, app_token, game_id, proxies) -> None:
        super().__init__()
        self.headers = GET_PROMO_HEADERS
        self.app_token = app_token
        self.game_id = game_id
        self.proxies = proxies
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
            self.post(URL_REGISTER_EVENT, json=get_event_data(game_id=self.game_id), proxies=self.proxies)
            data = {"promoId": self.game_id}
            response = self.post(URL_CREATE_CODE, json=data, proxies=self.proxies)
            if response.status_code == 200 and (promo := response.json().get('promoCode', '')):
                return promo
            time.sleep(1)
 

if __name__ == '__main__':
    wizard = PromoGenerator()
    print(wizard.get_promo())