# Настройки API
API_URL_INIT = 'https://zavod-api.mdaowallet.com/telegram/auth'
API_URL_CLAIM = 'https://zavod-api.mdaowallet.com/user/claim'
API_URL_FARM = 'https://zavod-api.mdaowallet.com/user/farm'
API_URL_PROFILE = 'https://zavod-api.mdaowallet.com/user/profile'
API_URL_UPGRADE_TOOLKIT = 'https://zavod-api.mdaowallet.com/user/upgradeToolkit'
API_URL_UPGRADE_WORKBENCH = 'https://zavod-api.mdaowallet.com/user/upgradeWorkbench'
API_URL_BURN_TOKENS = 'https://zavod-api.mdaowallet.com/guilds/burnTokens'
API_URL_MISSIONS = 'https://zavod-api.mdaowallet.com/missions'
API_URL_CLAIM_MISSION = 'https://zavod-api.mdaowallet.com/missions/claim/'
API_URL_CONFIRM_LINK_MISSION = 'https://zavod-api.mdaowallet.com/missions/confirm/link/'
API_URL_CONFIRM_TELEGRAM_MISSION = 'https://zavod-api.mdaowallet.com/missions/confirm/telegram/'
API_URL_WORKBENCH_SETTINGS = 'https://zavod-api.mdaowallet.com/farm/workbenchSettings'
API_URL_TOOLKIT_SETTINGS = 'https://zavod-api.mdaowallet.com/farm/toolkitSettings'
API_URL_GUILD_JOIN = 'https://zavod-api.mdaowallet.com/guilds/join'  # Добавлен API-URL для вступления в гильдию
API_URL_GAME_CRAFT = 'https://zavod-api.mdaowallet.com/craftGame'
API_URL_GAME_FIN = 'https://zavod-api.mdaowallet.com/craftGame/finishLevel'


# Messages
MSG_CLAIM = 'Забрали награду'
MSG_PROFILE = 'Обновили профиль'
MSG_STATE = 'Баланс: {balance}'
MSG_TOKENS = 'Монет: {tokens}'
MSG_TOOLKIT_LEVEL = 'Уровень инструментов: {tool}'
MSG_WORKBENCH_LEVEL = 'Уровень верстака: {work}'
MSG_GUILD = 'Гильдия: {guild}'
MSG_JOINED_GUILD = 'Вступили в гильдию'
MSG_UPGRADED_TOOLKIT = 'Улучшили инструменты'
MSG_UPGRADED_WORKBENCH = 'Улучшили верстак'
MSG_BURNED_TOKENS = 'Сожгли {tokens} монет'
MSG_CLAIMED_MISSION = 'Получили {prize} за {name}'
MSG_LINK_MISSION = 'Делаем задание на {prize} за {name}'
MSG_TELEGRAM_MISSION = 'Выполняем задание {name}'
MSG_GAME_START = 'Начали играть'


HEADERS = {

  'authority': 'zavod-api.mdaowallet.com',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,cy;q=0.6',
  'cache-control': 'no-cache',
  'origin': 'https://zavod.mdaowallet.com',
  'pragma': 'no-cache',
  'referer': 'https://zavod.mdaowallet.com/',
  'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
  'telegram-init-data': '',
  'user-agent': '',
}


# Error messages
MSG_ERROR_UPGRADING_TOOLKIT = 'Ошибка обновления инструментов: {error}'
MSG_ERROR_UPGRADING_WORKBENCH = 'Ошибка обновления верстака: {error}'
MSG_ERROR_BURNING_TOKENS = 'Ошибка сжигания монет: {error}'
MSG_ERROR_FETCHING_MISSIONS = 'Ошибка получения заданий: {error}'
MSG_ERROR_CLAIMING_MISSION = 'Ошибка получения задания {id}: {error}'
MSG_ERROR_CONFIRMING_LINK_MISSION = 'Ошибка подтверждения задания {id}: {error}'
MSG_ERROR_CONFIRMING_TELEGRAM_MISSION = 'Ошибка подтверждения задания {id}: {error}'

# Сообщения о включении/отключении
MSG_GAME_DISABLED = "Игра отключена."
MSG_UPGRADES_DISABLED = "Прокачка отключена."
MSG_TOOLKIT_UPGRADES_DISABLED = "Прокачка инструментов отключена."
MSG_WORKBENCH_UPGRADES_DISABLED = "Прокачка верстака отключена."
MSG_GUILD_JOIN_DISABLED = "Вступление в гильдию отключено."