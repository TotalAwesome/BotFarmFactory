### Что хочется видеть:
У каждого модуля должна быть похожая структура:

```
__init__.py
client.py
utils.py
strings.py
```
`__init__.py` - Инициализация пакета. Достаточно оставить файл пустым

`utils.py` - Опционален, здесь размещаем вспомогательные функции для работы модуля. Парсеры, конвертеры и т.д.

`strings.py` - Здесь храним все URL, строки сообщений, словари с данными. Большая просьба не размещать в самом коде строки в чистом виде. Гораздо приятнее видеть константы, редактировать их тоже удобнее в отдельном файле.

`client.py` - Ну а это сердце нашего модуля. Здесь и будет наш класс фармера. В этом файле обязательно описать класс `BotFarmer`. Именно он и будет импортироваться в фабрику при старте.

### Разработка
Для удобства разработки я сделал модуль-болванку и поместил в каталог `bots/template`:

```python
from bots.base.base import BaseFarmer
from bots.template.strings import HEADERS


class BotFarmer(BaseFarmer):
    name = "bot_username"
    extra_code = "ref_code"  # в случае если рефка вида https://t.me/bot_username?start=ref_code
    app_extra = "ref_code"  # в случае если рефка вида https://t.me/bot_username?action?param=ref_code (Это нужно доработать, но примеры есть среди ботов)
    initialization_data = {}  # данные для передачи в инициатор, отличаются в зависимости от типа кнопки входа в бота
    refreshable_token = False  # обновлять ли токен в боте
    codes_to_refresh = (401,)  # при получении этих статусов будет автоматически обновляться токен вызовом self.refresh_token()


    def set_headers(self, *args, **kwargs):
        """ Установка заголовков """
        self.headers = HEADERS.copy()

    def authenticate(self, *args, **kwargs):
        """ Аутентифифкация, получения токена, выставление заголовков, заполнение шаблона запроса и тд... """
        raise NotImplementedError

    def refresh_token(self):
        """ Метод вызывается для обновления токена, при условии что self.refreshable_token == True """
        raise NotImplementedError

    def set_start_time(self):
        """ 
        Метод выставляет время следующего захода фармера. 
        Например время когда закончится фарминг или накопятся тапы
        Время выставляется в формате timestamp
        time.time() + 60 это запуск через минуту
        """
        raise NotImplementedError

    def farm(self):
        """
        Основной метод, описывающий логику модуля. 
        Покупки, прокачки. Все здесь 
        """
        raise NotImplementedError
```

Для начала работ копируем каталог `template` и переименовываем в новый модуль.

# ...
