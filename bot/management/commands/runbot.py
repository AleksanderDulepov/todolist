import random
import string

from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from todolist.settings import TG_TOKEN


class Command(BaseCommand):

    def handle(self, *args, **options):
        offset = 0
        tg_client = TgClient(TG_TOKEN)
        while True:
            res = tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                message_obj = item.message

                # пользователь уже обращался к боту
                if TgUser.objects.filter(t_user_id=message_obj.from_id).exists():
                    obj = TgUser.objects.get(t_user_id=message_obj.from_id)

                    # пользователь уже авторизован
                    if obj.fk_user_id:
                        tg_client.send_message(chat_id=message_obj.chat.id, text="Пользователь авторизован")
                    # еще не авторизован
                    else:
                        v_code = self.get_ver_code()
                        tg_client.send_message(chat_id=message_obj.chat.id, text=f'[verification code] {v_code}')
                        obj.verification_code = v_code
                        obj.save()

                # пользователь еще не обращался к боту
                else:
                    v_code = self.get_ver_code()
                    tg_client.send_message(chat_id=message_obj.chat.id, text=f'[verification code] {v_code}')
                    TgUser.objects.create(t_chat_id=message_obj.chat.id, t_user_id=message_obj.from_id,
                                          verification_code=v_code)

    def get_ver_code(self) -> str:
        characters = string.ascii_letters + string.digits + string.punctuation
        v_code = ''.join(random.choice(characters) for i in range(15))
        return v_code
