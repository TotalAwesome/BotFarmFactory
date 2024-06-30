# BotFarmFactory
Небольшой "фрейемворк" для создания ферм по прокачке телеграм "тапалок"

Примерынй алгоритм действий:
1. Записать полученные аргументы в `config.py` (`config_local.py`)
2. Заполнить файл `accounts.py` (`accounts_local.py`) здесь нужен номер телефона на котором висит телеграм аккаунт и прокси, через который будут ходить все тапалки на этом аккаунте
3. Устновить python 3 (если вдруг не установлен, инструкции есть в интернете)
4. Установить зависимости выполнив команду в терминале `pip install -r requirements.txt`
5. Запустить фарминг `python3 factory.py`

После запуска, бот аутентифицируется в учетках телеграма и под каждой учеткой получает токены и прочие кредсы для доступа к ботам, с которыми бот умеет работать.

В данный момент реализованы боты:

- [cellcoin_bot](https://t.me/cellcoin_bot?start=102796269)
- [simple_tap_bot](https://t.me/Simple_Tap_Bot?start=1718085881160)
- [blum](https://t.me/BlumCryptoBot/app?startapp=ref_ItXoLRFElL)
- [iceberg](https://t.me/IcebergAppBot?start=referral_102796269)

Боты начнут последовательно фармить на каждом аккаунте

Если все выполнено правильно, вы увидите примерно следующую картину:
![image](https://github.com/TotalAwesome/BotFarmFactory/assets/39047158/a0e77b95-5ae1-4f64-b68d-cb904c0866b7)

Ответы почти на все вопросы уже есть в чате и в закрепе: https://t.me/CryptoAutoFarm

Для донатов: USDT TRC20: TTTMM1PXxNS7d3tAcruamT6GE8ye5BrZ4w
