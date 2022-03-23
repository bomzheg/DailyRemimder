from dataclasses import dataclass
from datetime import datetime
from typing import Any

from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, SwitchTo
from aiogram_dialog.widgets.text import Const, Format

TIME_PATTERN = "%H:%M"


class SettingsSG(StatesGroup):
    main = State()
    participants = State()
    timetable_time = State()
    timetable_days = State()


@dataclass
class Participant:
    tg_id: int
    db_id: int
    username: str
    name: str
    checked: bool = False

    @property
    def is_checked(self):
        return '✓' if self.checked else '✗'


users_db = {"users": [
    Participant(tg_id=666, db_id=1, username="bomzheg", name="Yuriy"),
    Participant(tg_id=42, db_id=2, username="alex", name="Alexey"),
]}

WEEKDAYS = ("ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС")


async def change_select(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer(f"clicked {item_id}")
    asked_id = int(item_id)
    for user in users_db["users"]:
        if user.tg_id == asked_id:
            user.checked = not user.checked


async def get_potential_participants(**kwargs):
    return users_db


async def get_weekdays(**kwargs):
    return {"weekdays": WEEKDAYS}


async def change_weekday(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer(f"clicked {item_id}")


async def get_time(m: Message, dialog_: Dialog, manager: DialogManager):
    try:
        time_ = datetime.strptime(m.text, TIME_PATTERN).time()
    except ValueError:
        await m.answer("Некорректный формат времени. Пожалуйста введите время в формате ЧЧ:ММ")
        return
    await manager.start(SettingsSG.timetable_time, dict(timetable={time_.strftime(TIME_PATTERN): []}))


async def get_result(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.current_context().start_data
    return {
        "my_time": data["timetable"] if data else "None",
    }


dialog = Dialog(
    Window(
        Const("Настройка ежедневного митинга"),
        SwitchTo(
            Const("Подписчики"),
            id="to_participants_ls",
            state=SettingsSG.participants,
        ),
        SwitchTo(
            Const("Расписание"),
            id="to_timetable",
            state=SettingsSG.timetable_time,
        ),
        state=SettingsSG.main,
    ),
    Window(
        Const("Подписчики"),
        SwitchTo(
            Const("Назад"),
            id="to_main",
            state=SettingsSG.main,
        ),
        ScrollingGroup(
            Select(
                Format("{item.is_checked}{item.name}"),
                id="participants",
                item_id_getter=lambda x: x.tg_id,
                items="users",
                on_click=change_select,
            ),
            id="participants_sg",
            width=1,
            height=10,
        ),
        getter=get_potential_participants,
        state=SettingsSG.participants,
    ),
    Window(
        Format("Введите время в формате ЧЧ:ММ\nБудет сохранено: {my_time}"),
        SwitchTo(
            Const("Назад"),
            id="to_main",
            state=SettingsSG.main,
        ),
        MessageInput(
            func=get_time,
        ),
        SwitchTo(
            Const("Далее"),
            id="to_timetable_days",
            state=SettingsSG.timetable_days,
        ),
        getter=get_result,
        state=SettingsSG.timetable_time,
    ),
    Window(
        Const("Выберите дни недели для данного времени"),
        SwitchTo(
            Const("В главное меню"),
            id="to_main",
            state=SettingsSG.main,
        ),
        Select(
            Format("{item}"),
            id="weekdays",
            item_id_getter=lambda x: x,
            items="weekdays",
            on_click=change_weekday,
        ),
        getter=get_weekdays,
        state=SettingsSG.timetable_days,
    )
)
