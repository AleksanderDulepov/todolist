import random
import string

from django.core.management import BaseCommand
from django.db.models import Q
from rest_framework.generics import get_object_or_404

from bot.models import TgUser, State
from bot.tg.client import TgClient
from goals.models import Goal, GoalCategory
from todolist.settings import TG_TOKEN


class Command(BaseCommand):
    tg_client = TgClient(TG_TOKEN)
    categories_list = []
    selected_category = None

    def handle(self, *args, **options):
        offset = 0
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                message_obj = item.message
                chat_id = message_obj.chat.id
                text = message_obj.text

                try:
                    obj = get_object_or_404(TgUser, t_user_id=message_obj.from_id)
                except:
                    # пользователь еще не обращался к боту
                    v_code = self.get_ver_code()
                    obj = TgUser.objects.create(t_chat_id=message_obj.chat.id,
                                                t_user_id=message_obj.from_id,
                                                verification_code=v_code,
                                                state=State.not_authorized)

                if obj.state == State.not_authorized:
                    # пользователь уже обращался к боту, но не авторизован
                    v_code = self.get_ver_code()
                    self.tg_client.send_message(chat_id=message_obj.chat.id, text=f'[verification code] {v_code}')
                    obj.verification_code = v_code
                    obj.save()

                if obj.state == State.authorized:
                    if text == "/goals":
                        goals_qs = Goal.objects.select_related('category__board').filter(
                            category__board__participants__user=obj.fk_user)
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
                            obj.state = State.input_category
                            obj.save()
                            # obj.update(state=State.input_category)
                            self.categories_list = categories_qs.all()
                            for i, category in enumerate(categories_qs):
                                categories_message += f"#{i + 1} {category.title} (доска {category.board.title})\n"
                        else:
                            categories_message = "Список категорий пуст"

                        self.tg_client.send_message(chat_id=chat_id, text=categories_message)

                    else:
                        self.tg_client.send_message(chat_id=chat_id, text="Неизвестная команда")
                    continue

                if obj.state == State.input_category:
                    # проверка группы
                    if text.isdigit() and int(text) in range(1, len(self.categories_list) + 1):
                        obj.state = State.input_title_goal
                        obj.save()
                        # obj.update(state=State.input_title_goal)
                        self.selected_category = self.categories_list[int(text) - 1]
                        self.tg_client.send_message(chat_id=chat_id, text="Введите название цели")


                    elif text == "/cancel":
                        is_create_goal_proc = False
                        self.tg_client.send_message(chat_id=chat_id, text="Операция отменена")
                        obj.state = State.authorized
                        obj.save()
                        self.categories_list = []
                        self.selected_category = None
                    else:
                        self.tg_client.send_message(chat_id=chat_id,
                                                    text="Ошибка выбора категории. Пожалуйста, повторите ввод")
                    continue

                if obj.state == State.input_title_goal:
                    try:
                        new_goal = Goal.objects.create(user=obj.fk_user, category=self.selected_category, title=text)
                        self.tg_client.send_message(chat_id=chat_id, text=f"#{new_goal.id} {new_goal.title}")
                        self.categories_list = []
                        self.selected_category = None
                        obj.state = State.authorized
                        obj.save()
                    except:
                        self.tg_client.send_message(chat_id=chat_id, text="Ошибка создания новой цели")

    def get_ver_code(self) -> str:
        characters = string.ascii_letters + string.digits
        v_code = ''.join(random.choice(characters) for i in range(15))
        return v_code
