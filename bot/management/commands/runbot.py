from django.core.management import BaseCommand
from rest_framework.generics import get_object_or_404
from bot.management.commands.service import TgDialog
from bot.models import TgUser, State


class Command(BaseCommand):
    """А сlass that includes method to provide telegram bot execution"""

    tg_handler = TgDialog()

    def handle(self, *args, **options) -> None:
        """A method to perform telegram bot relations"""

        offset = 0
        while True:
            res = self.tg_handler.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1

                message_obj = item.message
                chat_id = message_obj.chat.id
                text = message_obj.text



                try:
                    obj = get_object_or_404(TgUser, t_user_id=message_obj.from_id)
                except:
                    # пользователь еще не обращался к боту
                    obj = self.tg_handler.perform_introduction_action(chat_id, message_obj.from_id)

                if obj.state == State.not_authorized:
                    # пользователь уже обращался к боту, но не авторизован
                    self.tg_handler.perform_verification(obj, chat_id)

                if obj.state == State.authorized:
                    self.tg_handler.perform_main_menu_actions(obj, chat_id, text)
                    continue

                if obj.state == State.input_category:
                    self.tg_handler.create_goal(obj, chat_id, text)
                    continue

                if obj.state == State.input_title_goal:
                    self.tg_handler.input_title_goal(obj, chat_id, text)
