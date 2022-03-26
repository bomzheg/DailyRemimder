from dataclasses import dataclass
from datetime import datetime
from typing import Any

from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, Case

TIME_PATTERN = "%H:%M"
WEEKDAYS = {
    "MON": "ПН",
    "TUE": "ВТ",
    "WED": "СР",
    "THU": "ЧТ",
    "FRI": "ПТ",
    "SUT": "СБ",
    "SUN": "ВС",
}


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


async def change_select(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer(f"clicked {item_id}")
    asked_id = int(item_id)
    for user in users_db["users"]:
        if user.tg_id == asked_id:
            user.checked = not user.checked


async def get_potential_participants(**kwargs):
    return users_db


async def get_weekdays(dialog_manager: DialogManager, **kwargs):
    data: dict[str, Any] = dialog_manager.current_context().start_data
    days: list[str] = data["new_time"]["days"]
    return {"weekdays": [
        (('✓' if en_day in days else '✗') + ru_day, en_day) for en_day, ru_day in WEEKDAYS.items()
    ]}


async def change_weekday(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer(f"clicked {item_id}")
    data: dict[str, Any] = manager.current_context().start_data
    for i, day in enumerate(data["new_time"]["days"]):
        if day == item_id:
            data["new_time"]["days"].pop(i)
            return
    data["new_time"]["days"].append(item_id)


async def get_time(m: Message, dialog_: Dialog, manager: DialogManager) -> None:
    try:
        time_ = datetime.strptime(m.text, TIME_PATTERN).time()
    except ValueError:
        await m.answer("Некорректный формат времени. Пожалуйста введите время в формате ЧЧ:ММ")
        return
    await manager.start(
        SettingsSG.timetable_time,
        dict(new_time={"time": time_.strftime(TIME_PATTERN), "days": []}),
    )


async def get_saved_time(dialog_manager: DialogManager, **kwargs):
    data: dict[str, Any] = dialog_manager.current_context().start_data
    return {
        "my_time": data["new_time"]["time"] if data else "None",
        "has_data": bool(data),
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
        Case(
            {
                False: Const("Введите время в формате ЧЧ:ММ"),
                True: Format(
                    "Будет сохранено: {my_time}. "
                    "Нажмите \"Далее\", если уверены, "
                    "или отправьте другое время в формате ЧЧ:ММ вместо этого"
                ),
            },
            selector="has_data",
        ),
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
        getter=get_saved_time,
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
            Format("{item[0]}"),
            id="weekdays",
            item_id_getter=lambda x: x[1],
            items="weekdays",
            on_click=change_weekday,
        ),
        getter=get_weekdays,
        state=SettingsSG.timetable_days,
    )
)
