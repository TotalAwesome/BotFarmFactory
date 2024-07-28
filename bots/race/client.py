
from bots.base.base import BaseFarmer
from bots.base.utils import to_localtz_timestamp, api_response
from .strings import HEADERS, URL_DRIVE, URL_INFO, URL_INIT


class BotFarmer(BaseFarmer):
    name = "racememe_bot"
    extra_code = "r_102796269"
    init_data = None
    refreshable_token = False
    codes_to_refresh = (401,)
    initialization_data = dict(peer=name, bot=name, url=URL_INIT)

    def set_headers(self, *args, **kwargs):
        self.headers = HEADERS.copy()
        self.get = api_response(super().get)
        self.post = api_response(super().post)

    def authenticate(self, *args, **kwargs):
        auth_data = self.initiator.get_auth_data(**self.initialization_data)
        self.init_data = auth_data['url'].split('tgWebAppData=')[-1].split('&')[0]

    def refresh_token(self):
        self.initiator.connect()
        self.authenticate()
        self.initiator.disconnect()

    def set_start_time(self):
        """ 
        Метод выставляет время следующего захода фармера. 
        Например время когда закончится фарминг или накопятся тапы 
        """
        raise NotImplementedError

    def sync(self):
        response = self.get(URL_INFO.format(init_data=self.init_data))
        if response:
            self.info = response

    def farm(self):
        self.sync()
        pass
