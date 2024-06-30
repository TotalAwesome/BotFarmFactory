import os
import json
from telethon.sync import TelegramClient, functions, types
from urllib.parse import unquote, parse_qs, urlparse
from datetime import timedelta
from config import ACCOUNTS_DIR, TELEGRAM_AUTH


def username(dialog):
    username = str(getattr(dialog.message.chat, 'username', '_')).lower()
    return username


def parse_auth_data(url):
    return
    parsed_url = urlparse(url)
    full = parse_qs(parsed_url.fragment)
    full['tgWebAppVersion'] = full['tgWebAppVersion'][0]
    full['tgWebAppPlatform'] = full['tgWebAppPlatform'][0]
    full['tgWebAppData'] = parse_qs(full['tgWebAppData'][0])
    full['tgWebAppData']['query_id'] = full['tgWebAppData']['query_id'][0]
    full['tgWebAppData']['query_id'] = full['tgWebAppData']['auth_date'][0]
    full['tgWebAppData']['hash'] = full['tgWebAppData']['hash'][0]
    full['tgWebAppData']['user'] = json.loads(full['tgWebAppData']['user'][0])
    return full


class Initiator(TelegramClient):

    phone = None
    registered = []

    def __init__(self, phone):
        kwargs = {}
        if phone:
            self.phone = phone
            if not os.path.exists(ACCOUNTS_DIR):
                os.mkdir(ACCOUNTS_DIR)
            filename = os.path.join(ACCOUNTS_DIR, phone.strip('+'))
            super().__init__(session=filename, **TELEGRAM_AUTH)
            self.start(phone=self.phone)
        else:
            raise Exception('Provide a phone number ({})'.format(str(kwargs)))
    
    def is_bot_registered(self, botname=None):
        botname = botname.lower()
        if botname not in self.registered:
            dialogs = self.get_dialogs()
            is_registered = any(map(lambda x: username(x) == botname, dialogs))
            if is_registered:
                self.registered.append(botname)
        return botname in self.registered

    def prepare_bot(self, *args):
        if self.is_bot_registered(args[0]):
            return
        request = functions.messages.StartBotRequest(*args)
        self(request)

    def get_auth_data(self, **kwargs):
        
        kwargs['platform'] = kwargs.get('platform', 'android')
        kwargs['from_bot_menu'] = kwargs.get('from_bot_menu', True)
        if self.is_bot_registered and 'start_param' in kwargs:
            kwargs['start_param'] = ''
        if not 'app' in kwargs:
            web_app = self(functions.messages.RequestWebViewRequest(**kwargs))
        else:
            kwargs.pop('from_bot_menu')
            web_app = self(functions.messages.RequestAppWebViewRequest(**kwargs))
        structured = parse_auth_data(web_app.url)
        auth_data = web_app.url.split('#tgWebAppData=')[1].replace("%3D","=").split('&tgWebAppVersion=')[0].replace("%26","&")
        user = auth_data.split("user=")[1].split("&")[0]
        return {"userId": self._self_id, "authData": auth_data.replace(user, unquote(user))}

