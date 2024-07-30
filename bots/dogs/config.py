try:
    from bots.dogs.config_local import TASK_EXCLUDE
except:
    TASK_EXCLUDE = []


'''

Последовательность действий:
1. Создайте файл config_local.py
2. Пример содержимого:

TASK_EXCLUDE = [
    "notcoin-tier-gold",
    "notcoin-tier-platinum",
    "add-bone-telegram",
    "invite-frens",
    "subscribe-notcoin",
]

В результате, ваш конфиг не будет перезатираться при обновлении фабрики.
Можете добавлять/убирать по аналогии таски, которые бот не может выполнить.
Название таска берем из сообщения в логе, например: "...Ошибка задания invite-frens"
invite-frens - название таска.

'''