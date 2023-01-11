import random
import string
from typing import List

from django.db.models import Q

from bot.models import TgUser, State
from bot.tg.client import TgClient
from goals.models import GoalCategory, Goal
from todolist.settings import TG_TOKEN


class TgDialog():
    """
    А сlass that includes service methods

    Attributes
    --------
    tg_clent: TgClient
        An object that performs queries to telegram bot api
    categories_list: List[Goal_category]
        A sequence of Goal_category objects that can be offered to select user when creating goal in telegram bot
    selected_category: Goal_category
        A user's selected Goal_category object
    """

    def __init__(self) -> None:
        """A method to initialize variables when creating the object"""

        self.tg_client: TgClient = TgClient(TG_TOKEN)
        self.categories_list: List[GoalCategory] = []
        self.selected_category: GoalCategory = None

    def get_ver_code(self) -> str:
        """A method to get validation code that includes 15 random letters and digits"""

        characters = string.ascii_letters + string.digits
        v_code = ''.join(random.choice(characters) for i in range(15))
        return v_code

    def perform_introduction_action(self, chat_id: str, user_id: str) -> TgUser:
        """A method that creates new user record from telegram bot to database"""

        v_code = self.get_ver_code()
        obj = TgUser.objects.create(t_chat_id=chat_id,
                                    t_user_id=user_id,
                                    verification_code=v_code,
                                    state=State.not_authorized)
        return obj

    def perform_verification(self, obj: TgUser, chat_id: str) -> None:
        """A method that sends verification code to telegram bot chat and save it in database"""

        v_code = self.get_ver_code()
        self.tg_client.send_message(chat_id=chat_id, text=f'[verification code] {v_code}')
        obj.verification_code = v_code
        obj.save()

    def perform_main_menu_actions(self, obj: TgUser, chat_id: str, text: str) -> None:
        """A method that manages actions authorized users in telegram bot chat"""

        if text == "/goals":
            goals_qs = Goal.objects.select_related('category__board').filter(
                category__board__participants__user=obj.fk_user).order_by("id")
            goals_message = ""
            if goals_qs.count() > 0:
                for goal in goals_qs:
                    goals_message += f"#{goal.id} {goal.title}\n"
            else:
                goals_message = "Список целей пуст"

            self.tg_client.send_message(chat_id=chat_id, text=goals_message)

        elif text == "/create":
            categories_qs = GoalCategory.objects.select_related('user', 'board').filter(
                Q(board__participants__user=obj.fk_user) & Q(board__is_deleted=False))
            categories_message = ""
            if categories_qs.count() > 0:
                self.return_base_state(obj, State.input_category)
                self.categories_list = categories_qs.all()
                for i, category in enumerate(categories_qs):
                    categories_message += f"#{i + 1} {category.title} (доска {category.board.title})\n"
            else:
                categories_message = "Список категорий пуст"

            self.tg_client.send_message(chat_id=chat_id, text=categories_message)

        else:
            self.tg_client.send_message(chat_id=chat_id, text="Неизвестная команда")

    def create_goal(self, obj: TgUser, chat_id: str, text: str) -> None:
        """A method that checks category"""

        if text.isdigit() and int(text) in range(1, len(self.categories_list) + 1):
            self.return_base_state(obj, State.input_title_goal)
            self.selected_category = self.categories_list[int(text) - 1]
            self.tg_client.send_message(chat_id=chat_id, text="Введите название цели")

        elif text == "/cancel":
            self.cancel_action(obj, chat_id, text)

        else:
            self.tg_client.send_message(chat_id=chat_id,
                                        text="Ошибка выбора категории. Пожалуйста, повторите ввод")

    def input_title_goal(self, obj: TgUser, chat_id: str, text: str) -> None:
        """A method that provides creating new goal object"""

        if text == "/cancel":
            self.cancel_action(obj, chat_id, text)
        else:
            try:
                new_goal = Goal.objects.create(user=obj.fk_user, category=self.selected_category, title=text)
                self.tg_client.send_message(chat_id=chat_id, text=f"#{new_goal.id} {new_goal.title}")
                self.clear_buffer()
                self.return_base_state(obj)
            except:
                self.tg_client.send_message(chat_id=chat_id, text="Ошибка создания новой цели")
                self.clear_buffer()
                self.return_base_state(obj)

    def cancel_action(self, obj: TgUser, chat_id: str, text: str) -> None:
        """A method that provides interrupting of action"""

        self.tg_client.send_message(chat_id=chat_id, text="Операция отменена")
        self.return_base_state(obj)
        self.clear_buffer()

    def clear_buffer(self) -> None:
        """A method that performs clearing buffer after execution or interrapting of action"""

        self.categories_list = []
        self.selected_category = None

    def return_base_state(self, obj: TgUser, state=State.authorized) -> None:
        """A method that changes given object's state attribute"""

        obj.state = state
        obj.save()