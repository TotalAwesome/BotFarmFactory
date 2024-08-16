"""
    FEATURES:
        1. buy_upgrades -> включение/отключение покупки карточек
        2. buy_decision_method -> метод покупки карточек (
            - price -> покупать самую дешевую
            - payback -> покупать ту, что быстрей всего окупится
            - profit -> покупать самую прибыльну
            - profitness -> покупать самую профитную (сколько добыча на каждый потраченный хома-рубль)
            )
        3. delay_between_attempts -> Задержка между заходами в секундах
        4. percent_to_spend -> Процент от депозита который можно потратить за 1 подход
        5. taps -> включение/отключение тапов
        6. max_upgrade_payback - максимальная окупаемость апргейда в часах
        7. buy_skins - покупать скины
        8. apply_promo - получать и применять промокоды для игр
    
"""


FEATURES = {
    "buy_upgrades": True,
    "buy_decision_method": "payback",
    "delay_between_attempts": 60 * 10,
    "percent_to_spend": 10,
    "taps": True,
    "max_upgrade_payback": 24*100,
    "buy_skins": False,
    "apply_promo": False,
    "minimum_farm_sleep": 2 * 60 * 60, # (2 часа) минимальная задержка до следующего захода 
    "maximum_farm_sleep": 3 * 60 * 60, # (6 часов) максимальная задержка до следующего захода
    "minimum_upgrade_delay": 5, # (5 секунд) минимальная задержка между апгрейдами
    "maximum_upgrade_delay": 10, # (10 секунд) максимальная задержка между апгрейдами
}


try:
    from bots.hamster_kombat.config_local import *
except ImportError:
    pass