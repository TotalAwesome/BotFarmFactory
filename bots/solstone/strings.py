URL_INIT = "https://solstone-app.gleam.bot"
URL_AUTH = "https://solstone-api.gleam.bot/auth"
URL_TASKS = "https://solstone-api.gleam.bot/quests?project=SolStone"
URL_CLAIM_TASK = "https://solstone-api.gleam.bot/complete-quest"
URL_START_FARM = "https://solstone-api.gleam.bot/start-farming"
URL_CLAIM_FARMED = "https://solstone-api.gleam.bot/claim"
URL_CLAIM_REFS = "https://solstone-api.gleam.bot/claim-ref-rewards"
URL_REFS_INFO = "https://solstone-api.gleam.bot/users/{tg_id}/invitees?project=SolStone"

HEADERS = {
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,cy;q=0.6',
  'cache-control': 'no-cache',
  'content-type': 'application/json',
  'ngrok-skip-browser-warning': '69420',
  'origin': 'https://solstone-app.gleam.bot',
  'pragma': 'no-cache',
  'priority': 'u=1, i',
  'referer': 'https://solstone-app.gleam.bot/',
  'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
  'sec-ch-ua-mobile': '?1',
  'sec-ch-ua-platform': '"Android"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
  'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRXN8N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36',
}

MSG_CLAIM_FARMED = "Собрал нафармленное"
MSG_FARMING_STARTED = "Начал фармить"
MSG_TASK_CLAIMED = "Собрал за таску {amount}"
MSG_CLAIM_REFS = "Собрал за рефов {amount}"