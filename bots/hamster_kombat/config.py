"""
    FEATURES:
        1. buy_upgrades -> включение/отключение покупки карточек
        2. buy_decision_method -> метод покупки карточек (
            - price -> покупать самую дешевую
            - payback -> покупать ту, что быстрей всего окупится
            - profit -> покупать самую прибыльну
            - profitness -> покупать самую профитную (сколько добыча на каждый потраченный хома-рубль)
            )
        3. taps -> включение/отключение тапов
        4. max_upgrade_payback - максимальная окупаемость апргейда в часах, например 40*100. По умолчанию - не ограничена.
        5. buy_skins - покупать скины
        6. блок, отвечающий за таймауты
        7. buy_skins - покупать скины
"""


FEATURES = {
    "buy_upgrades": True,
    "buy_decision_method": "payback",
    "taps": True,
    "max_upgrade_payback": None,
    "buy_skins": False,
    "max_skin_price": 10_000_000,
    "minimum_farm_sleep": 2 * 60 * 60, # (2 часа) минимальная задержка до следующего захода 
    "maximum_farm_sleep": 3 * 60 * 60, # (6 часов) максимальная задержка до следующего захода
    "minimum_upgrade_delay": 5, # (5 секунд) минимальная задержка между апгрейдами
    "maximum_upgrade_delay": 10, # (10 секунд) максимальная задержка между апгрейдами
}


try:
    from bots.hamster_kombat.config_local import *
except ImportError:
    pass