import os
from telethon.sync import TelegramClient, functions, types
from urllib.parse import unquote
from datetime import timedelta

from config import ACCOUNTS_DIR, TELEGRAM_AUTH

class Initiator(TelegramClient):

    phone = None

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
    
    def prepare_bot(self, *args):
        self.do_not_disturb(args[0])
        request = functions.messages.StartBotRequest(*args)
        self(request)

    def get_auth_data(self, **kwargs):
        
        kwargs['platform'] = kwargs.get('platform', 'android')
        kwargs['from_bot_menu'] = kwargs.get('from_bot_menu', True)
        if kwargs.get('start_param') is None:
            web_app = self(functions.messages.RequestWebViewRequest(**kwargs))
        else:
            kwargs.pop('from_bot_menu')
            web_app = self(functions.messages.RequestAppWebViewRequest(**kwargs))
        auth_data = web_app.url.split('#tgWebAppData=')[1].replace("%3D","=").split('&tgWebAppVersion=')[0].replace("%26","&")
        user = auth_data.split("user=")[1].split("&")[0]
        return {"userId": self._self_id, "authData": auth_data.replace(user, unquote(user))}

    def do_not_disturb(self, peer):
        self(functions.account.UpdateNotifySettingsRequest(
            peer=peer,
            settings=types.InputPeerNotifySettings(
                mute_until=timedelta(minutes=5),
                silent=True
            )))