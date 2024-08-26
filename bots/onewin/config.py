UPGRADE_MAX_LEVEL = 20

try:
    from bots.onewin.config_local import FEATURES
except:

    FEATURES = {
        "minimum_delay": 3 * 60 * 60, # (3 часа) минимальная задержка до следующего захода 
        "maximum_delay": 6 * 60 * 60, # (6 часов) максимальная задержка до следующего захода
        "get_daily_reward": True, # забирать ежедневную награду
        "buy_upgrades": True, # покупать апргейды
        "buy_decision_method": "payback", # логика выбора апгрейдов
        "num_purchases_per_cycle": 10, # количество покупок апгрейдов за циклв
        "max_upgrade_cost": 5_000_000, # максимальная стоимость апгрейда
        "max_upgrade_payback": 5_000, # максимальная окупаемость апгрейда в часах
        "min_cash_value_in_balance": 10_000, # минимальный остаток после апгрейда
        "blind_upgrade": True, # попытка покупки 1 уровня нового здания, основываясь на хардкодных данных
        "friends_claim": True # забирать награду от рефов
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