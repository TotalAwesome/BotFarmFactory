BUY_UPGRADES = True  # Покупать ли апгрейды
PERCENT_TO_SPEND = 100  # Какой процент от депозита должен остаться после покупок


try:
    from bots.simple.config_local import TASK_EXCLUDE
except:
    # вносим id или title квеста
    TASK_EXCLUDE = [
        "Invite one more friend",
        6270925024, # Пригласи одного или нескольких друзей
        6270925049, # Войди в приложение через магазин
        6270925048, # Опубликуй историю в Instagram
        6270925017, # Найди и установи Simple
        6270925046, # Заполни email
        6270925011, # Подпишись на Simple Telegram
        6270925012, # Подпишись на канал co-CEO Simple!
        6270925013, # Непонятно что это:)
        6270925038, # Join BOOMS Game
    ]