"""
    https://github.com/TotalAwesome/BotFarmFactory
    https://t.me/CryptoAutoFarm
"""

from time import sleep
from importlib import import_module
from random import random, shuffle
from os import path, listdir

from initiator import Initiator
from accounts import TELEGRAM_ACCOUNTS
from bots.base.base import logging
from bots.base.utils import check_proxy
from config import ENABLED_BOTS

bots = []

if path.isdir("bots"):
    for directory in listdir("bots"):
        if directory == 'template':
            continue
        if ENABLED_BOTS and directory not in ENABLED_BOTS:
            continue
        try:
            module = import_module(f"bots.{directory}.client")
            bots.append(module.BotFarmer)
        except ImportError:
            pass
        except Exception as e:
            logging.error(e)
else:
    raise Exception("No bots :(")


def make_account_farmers(account):
    
    phone = account['phone']
    if proxy := account.get('proxy'):
        proxies = dict(http=proxy, https=proxy)
        proxy = proxy if check_proxy(proxies=proxies) else None
    try:
        initiator = Initiator(phone)
    except Exception as e:
        logging.error(f'{phone} Error: {e}')
        return []
    farmers = []
    for farmer_class in bots:
        try:
            farmer = farmer_class(initiator=initiator, proxy=proxy)
        except Exception as e:
            logging.error(f'{farmer_class.name} init error: {e}')
            continue
        if not farmer.is_alive:
            continue
        farmers.append(farmer)
    initiator.disconnect()
    sleep(random() * 10)
    return farmers
    

farmers = []
for account in TELEGRAM_ACCOUNTS:
    farmers += make_account_farmers(account)

print('')
logging.info("Найдены фармеры: {farmer_names}".format(
    farmer_names=", ".join(set([farmer.name.lower() for farmer in farmers])))
    )
    
if not farmers:
    exit()

while True:
    shuffle(farmers)
    for farmer in farmers:
        farmer.proceed_farming()
        sleep(1 + random())
    sleep(1)
