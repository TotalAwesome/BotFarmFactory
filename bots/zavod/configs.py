# configs.py

# Настройки бота
BOT_NAME = 'Mdaowalletbot'  # Имя бота
EXTRA_CODE = "102796269"  # Дополнительный код (если нужен)


# Настройки гильдии
GUILD_ID = 81  # ID гильдии, в которую бот должен вступить
ENABLE_GUILD_JOIN = True  # Включить/отключить вступление в гильдию

# Настройки задержек
SLEEP_TIME_CLAIM = 1  # Задержка после получения награды
SLEEP_TIME_FARM = 2  # Задержка после обновления информации о ферме
SLEEP_TIME_UPGRADE = 2  # Задержка после улучшения верстака или инструментов

# Настройки уровня для сжигания монет
TOOLKIT_LEVEL_BURN = 5  # Уровень инструментов, при котором бот начинает сжигать монеты
WORKBENCH_LEVEL_BURN = 49  # Уровень верстака, при котором бот начинает сжигать монеты 

# Включение/выключение прокачки и игры
ENABLE_UPGRADES = True  # Включить/отключить прокачку (верстака, инструментов)
ENABLE_GAME = True  # Включить/отключить игру
ENABLE_TASK = True  # Включить/отключить выполнение заданий
ENABLE_UP = True  # Включить/отключить получение награды

# Отдельно включаем прокачку верстака и инструментов
ENABLE_WORKBENCH_UPGRADE = True  # Включить/отключить прокачку верстака
ENABLE_TOOLKIT_UPGRADE = True  # Включить/отключить прокачку инструментов

# Время следующего запуска (в секундах)
MIN_WAIT_TIME = 1800  # минимальное время следующего захода в секундах (30 мин)
MAX_WAIT_TIME = 7200  # максимальное время следующего захода в секундах (2 час)