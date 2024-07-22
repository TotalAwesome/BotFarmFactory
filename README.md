# BotFarmFactory
Небольшой "фрейемворк" для создания ферм по прокачке телеграм "тапалок"

Примерынй алгоритм действий:
1. В `config.py` находится конфигурация клиента Telegram, ее желательно не трогать. Так же есть флаг DEBUG. (при значении True будет писать диагностическую информацию в файл debug.log)
2. Заполнить файл `accounts.py` (`accounts_local.py`) здесь нужен номер телефона на котором висит телеграм аккаунт и прокси, через который будут ходить все тапалки на этом аккаунте
3. Устновить python 3 (если вдруг не установлен, инструкции есть в интернете)
4. Установить зависимости выполнив команду в терминале `pip install -r requirements.txt` (если перекачали скрипт, стоит каждый раз это выполнять. может измениться набор пакетов)
5. Запустить фарминг `python3 factory.py`

После запуска, бот аутентифицируется в учетках телеграма и под каждой учеткой получает токены и прочие кредсы для доступа к ботам, с которыми бот умеет работать.

В данный момент реализованы боты:

- [cellcoin_bot](https://t.me/cellcoin_bot?start=102796269)
- [simple_tap_bot](https://t.me/Simple_Tap_Bot?start=1718085881160)
- [blum](https://t.me/BlumCryptoBot/app?startapp=ref_ItXoLRFElL)
- [iceberg](https://t.me/IcebergAppBot?start=referral_102796269)
- [MDAO Wallet (ZAVOD)](https://t.me/Mdaowalletbot?start=102796269)
- [anon](https://t.me/AnonEarnBot) (Если не регается, ищем рефки в интернете)
- [hamster kombat](https://t.me/Hamster_kombat_bot/start?startapp=kentId102796269)
- [TapCoinsBot](https://t.me/tapcoinsbot/app?startapp=ref_QjG2zG)
- [HEXN](https://t.me/hexn_bot/app?startapp=63b093b0-fcb8-41b5-8f50-bc61983ef4e3)

Боты начнут последовательно фармить на каждом аккаунте

Если все выполнено правильно, вы увидите примерно следующую картину:
![image](https://github.com/TotalAwesome/BotFarmFactory/assets/39047158/a0e77b95-5ae1-4f64-b68d-cb904c0866b7)

Ответы почти на все вопросы уже есть в канале или в чате и в закрепе: https://t.me/cryptoearnfactory

Для донатов: USDT TRC20: TTTMM1PXxNS7d3tAcruamT6GE8ye5BrZ4w
