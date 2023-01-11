from dataclasses import dataclass
from typing import List
from aiogram.types import Update, Message
import marshmallow as marshmallow


@dataclass
class GetUpdatesResponse:
    """
    А сlass that includes attributes from telegram bot api objects

    Attributes
    --------
    ok: bool
    	A variable that describes response status
    result: List[Update]
    	A sequence of Update objects that can be get from telegram bot request
    """

    ok: bool
    result: List[Update]

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class SendMessageResponse:
    """
    А сlass that includes Message objects from telegram bot

    Attributes
    --------
    ok: bool
    	A variable that describes response status
    result: List[Message]
    	A sequence of Message objects that can be get from telegram bot request
    """

    ok: bool
    result: Message

    class Meta:
        unknown = marshmallow.EXCLUDE

