from dataclasses import dataclass
from typing import List
from aiogram.types import Update, Message
import marshmallow as marshmallow


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[Update]

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    class Meta:
        unknown = marshmallow.EXCLUDE

