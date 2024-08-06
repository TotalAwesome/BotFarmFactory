UPGRADE_MAX_LEVEL = 20

try:
    from config_local import FEATURES
except:

    FEATURES = {
        "minimum_delay": 3*60*60, #3 часа
        "maximum_delay": 6*60*60, #6 часов
        "get_daily_reward": True,
        "buy_upgrades": True,
        "buy_decision_method": "payback",
        "num_purchases_per_cycle": 10,
        "max_upgrade_cost": 500_000,
        "max_upgrade_payback": 3600,
        "min_cash_value_in_balance": 10_000, 
    }


'''
Если хочется установить свои параметры для модуля, последовательность действий:
1. Создайте файл config_local.py
2. Пример содержимого:

FEATURES = [
    "get_daily_reward": True,
]

В результате, ваш конфиг не будет перезатираться при обновлении фабрики.

'''