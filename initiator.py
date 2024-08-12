import os
import json
from time import sleep
from telethon.sync import TelegramClient, functions, types
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest
from telethon.errors import FloodWaitError
from urllib.parse import unquote, parse_qs, urlparse
from datetime import timedelta
from config import ACCOUNTS_DIR, TELEGRAM_AUTH
from bots.base.base import logging


def username(dialog):
    username = str(getattr(dialog.message.chat, 'username', '_')).lower()
    return username


def catch_flood_error(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except FloodWaitError as e:
                logging.INFO(f'Флудим, подождем {e.seconds} секунд')
                sleep(e.seconds)
    return wrapper


class Initiator(TelegramClient):

    phone = None
    registered = []
    dialogs = None

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

    @catch_flood_error
    def is_bot_registered(self, botname=None):
        if not botname:
            return
        botname = botname.lower()
        if botname not in self.registered:
            self.dialogs = self.dialogs or self.get_dialogs()
            is_registered = any(map(lambda x: username(x) == botname, self.dialogs))
            if is_registered:
                self.registered.append(botname)
        return botname in self.registered

    @catch_flood_error
    def prepare_bot(self, *args):
        if self.is_bot_registered(args[0]):
            return
        request = functions.messages.StartBotRequest(*args)
        self(request)

    @catch_flood_error
    def get_auth_data(self, **kwargs):
        kwargs['platform'] = kwargs.get('platform', 'android')
        kwargs['from_bot_menu'] = kwargs.get('from_bot_menu', False)
        dicted = kwargs.pop('dicted', None)
        if not 'app' in kwargs:
            web_app = self(functions.messages.RequestWebViewRequest(**kwargs))
        else:
            kwargs.pop('from_bot_menu')
            web_app = self(functions.messages.RequestAppWebViewRequest(**kwargs, write_allowed=True))
        auth_data = web_app.url.split('#tgWebAppData=')[1].replace("%3D","=").split('&tgWebAppVersion=')[0].replace("%26","&")
        user = auth_data.split("user=")[1].split("&")[0]
        return {"userId": self._self_id, "authData": auth_data.replace(user, unquote(user)), 'url': web_app.url}

    @catch_flood_error
    def join_group(self, group_link):
        self(JoinChannelRequest(group_link))

    @catch_flood_error
    def subscribe_channel(self, channel_link):
        self(JoinChannelRequest(channel_link))
