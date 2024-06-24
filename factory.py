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


def import_bots():
    farmer_classes = []
    if path.isdir('bots'):
        for directory in listdir('bots'):
            try:
                module = import_module(f"bots.{directory}.client")
                farmer_classes.append(module.BotFarmer)
            except ImportError:
                pass
    else:
        raise Exception('No bots :(')
    return farmer_classes
    

def make_account_farmers(account):
    phone = account['phone']
    proxy = account.get('proxy')
    initiator = Initiator(phone)
    farmers = []
    bots = import_bots()
    for farmer_class in bots:
        farmers.append(farmer_class(initiator=initiator, proxy=proxy))
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

while True:
    shuffle(farmers)
    for farmer in farmers:
        farmer.proceed_farming()
        sleep(1 + random())
    sleep(1)
