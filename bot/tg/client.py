import json

import requests
from aiogram.types import Update, Message

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse


class TgClient:
    """
    А сlass that includes methods to execute connection with telegram bot

    Attributes
    --------
    token: str
    	A secret key to connection telegram bot
    """

    def __init__(self, token):
        """A method to initialize token variable while creating object"""

        self.token = token

    def get_url(self, method: str):
        """A method to get url to request to telegram bot api"""

        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        """A method to get Update objects from telegram bot request"""

        try:
            response = requests.get(self.get_url("getUpdates"), params={'offset': offset, 'timeout': timeout})
            res_dict = json.loads(response.content)
            object = GetUpdatesResponse(ok=res_dict.get("ok"), result=[Update(**i) for i in res_dict.get("result")])
            return object
        except:
            raise NotImplementedError

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        """A method to send message to telegram bot"""

        try:
            response = requests.get(self.get_url("sendMessage"), params={'chat_id': chat_id, 'text': text})
            res_dict = json.loads(response.content)
            object = SendMessageResponse(ok=res_dict.get("ok"), result=Message(**res_dict.get("result")))
            return object
        except:
            raise NotImplementedError
