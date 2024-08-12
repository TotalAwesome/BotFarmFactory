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
    
    TOKENS:
        name -> Название аккаунта. Так он будет виден в логе
        token -> токен аккаунта
        proxies -> настройки прокси, "кто знает - тот поймет". Если не нужен прокси, лучше убрать
"""


FEATURES = {
    "buy_upgrades": True,
    "buy_decision_method": "payback",
    "delay_between_attempts": 60 * 10,
    "percent_to_spend": 10,
    "taps": True,
    "max_upgrade_payback": 24*100,
}


try:
    from bots.hamster_kombat.config_local import *
except ImportError:
    pass