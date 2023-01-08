import json

import requests
from aiogram.types import Update, Message

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse


class TgClient:
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        try:
            response=requests.get(self.get_url("getUpdates"), params={'offset':offset,'timeout':timeout})
            res_dict = json.loads(response.content)
            object = GetUpdatesResponse(ok=res_dict.get("ok"), result=[Update(**i) for i in res_dict.get("result")])
            return object
        except:
            raise NotImplementedError


    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        try:
            response = requests.get(self.get_url("sendMessage"), params={'chat_id': chat_id, 'text': text})
            res_dict=json.loads(response.content)
            object = SendMessageResponse(ok=res_dict.get("ok"), result=Message(**res_dict.get("result")))
            return object
        except:
            raise NotImplementedError
