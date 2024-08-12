URL_INIT = "https://game.orbitonx.com/"
URL_AUTH = "https://api.orbitonx.com/api/auth"  # POST payload
URL_BALANCE = "https://api.orbitonx.com/api/users/balance"  # GET
URL_INFO = "https://api.orbitonx.com/api/users/info"  # GET
URL_REWARD = "https://api.orbitonx.com/api/users/reward"  # POST None
URL_STOCKS = "https://api.orbitonx.com/api/general/stocks"  # GET
URL_QUESTS = "https://api.orbitonx.com/api/user-quests"  # GET
URL_STAKING_CLAIM = "https://api.orbitonx.com/api/user-coins/collect-reward"  # PATCH
URL_TAP = "https://api.orbitonx.com/api/user-coins"  # POST payload
URL_TASKS = "https://api.orbitonx.com/api/user-tasks"  # GET
URL_TASK_CLAIM = "https://api.orbitonx.com/api/user-tasks/get-bonus/{id}"  # GET
URL_START_TASK = "https://api.orbitonx.com/api/user-tasks"  # POST
URL_WATCH_AD = "https://api.orbitonx.com/api/users/increase-balance"  # GET LOL
URL_CARDS_LIST = "https://api.orbitonx.com/api/boost-cards"
URL_MY_CARDS = "https://api.orbitonx.com/api/user-boost-cards"
URL_COMBOS = "https://api.orbitonx.com/api/combos"
URL_STOCKS = "https://api.orbitonx.com/api/general/stocks"

MSG_AUTH_ERROR = "Ошибка аутентификации"
MSG_STAKING_CLAIMED = "Собрал за стейкинг {rewardFromStacking}"
MSG_STAKING_STARTED = "Начал стейкать"
MSG_STAKING_TAP = "Натапал на стейкинг"
MSG_TASK_CLAIMED = "Выполнил таску на {capacity} $RCT"
MSG_WATCHED_AD = "Посмотрел рекалму ;) получил 10 $RCT"
MSG_BALANCE = "Текущий баланс: {balance}"

HEADERS = {
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,cy;q=0.6',
  'cache-control': 'no-cache',
  'content-type': 'application/json',
  'origin': 'https://game.orbitonx.com',
  'pragma': 'no-cache',
  'priority': 'u=1, i',
  'referer': 'https://game.orbitonx.com/',
  'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
  'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
  'x-timezone': 'Europe/Moscow',
}
