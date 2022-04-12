import json
from datetime import datetime
from typing import Any

from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.context.context import Context
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, SwitchTo, Button
from aiogram_dialog.widgets.text import Const, Format, Case

from app.dao import HolderDao
from app.models import dto
from app.rendering import render_bool
from app.services.meetings import get_available_meetings
from app.services.meetings_participants import turn_participant, get_available_participants

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
    meetings = State()
    meeting_main = State()
    participants = State()
    timetable = State()
    timetable_time = State()
    timetable_days = State()


async def change_select_user(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer()
    data = manager.data
    await turn_participant(
        data["dao"], data["chat"], manager.current_context().dialog_data["editing_meeting_id"], int(item_id),
    )


async def change_select_meetings(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer()
    data = manager.current_context().start_data
    if not isinstance(data, dict):
        data = {}
    data["editing_meeting_id"] = int(item_id)
    await manager.update(data)
    await manager.switch_to(SettingsSG.meeting_main)


async def get_potential_participants(dao: HolderDao, chat: dto.Chat, dialog_manager: DialogManager, **kwargs):
    return {"users": (await get_available_participants(
        dao, chat, dialog_manager.current_context().dialog_data["editing_meeting_id"]
    ))}


async def get_meetings(dao: HolderDao, chat: dto.Chat, **kwargs):
    return {"meetings": await get_available_meetings(dao, chat)}


async def get_weekdays(dialog_manager: DialogManager, **kwargs):
    data: dict[str, Any] = dialog_manager.current_context().dialog_data
    days: list[str] = data["new_time"]["days"]
    return {"weekdays": [
        (render_bool(en_day in days) + ru_day, en_day) for en_day, ru_day in WEEKDAYS.items()
    ]}


async def change_weekday(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer(f"clicked {item_id}")
    data: dict[str, Any] = manager.current_context().dialog_data
    for i, day in enumerate(data["new_time"]["days"]):
        if day == item_id:
            data["new_time"]["days"].pop(i)
            return
    data["new_time"]["days"].append(item_id)


async def get_time(m: Message, dialog_: Any, manager: DialogManager) -> None:
    try:
        time_ = datetime.strptime(m.text, TIME_PATTERN).time()
    except ValueError:
        await m.answer("Некорректный формат времени. Пожалуйста введите время в формате ЧЧ:ММ")
        return
    data = manager.current_context().start_data
    if not isinstance(data, dict):
        data = {}
    data['new_time'] = {"time": time_.strftime(TIME_PATTERN), "days": []}
    await manager.update(data)
    await manager.switch_to(SettingsSG.timetable_time)


async def get_saved_time(dialog_manager: DialogManager, **kwargs):
    data: dict[str, Any] = dialog_manager.current_context().dialog_data
    my_time = data.get("new_time", {}).get("time", None)
    return {
        "my_time": my_time if my_time else "None",
        "has_data": bool(my_time),
    }


async def save_time(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await c.answer()
    data: dict[str, Any] = dialog_manager.current_context().dialog_data
    timetable = data.setdefault("timetable", [])
    timetable.append(data.pop("new_time"))
    await dialog_manager.switch_to(SettingsSG.meeting_main)


async def get_timetable(dialog_manager: DialogManager, **kwargs):
    data: dict[str, Any] = dialog_manager.current_context().dialog_data
    timetable = data.get("timetable", [])
    return {
        "timetable": render_timetable(timetable),
        "has_timetable": bool(timetable),
    }


def render_timetable(data: list[dict[str, str | list[str]]]) -> str:
    return json.dumps(data)


async def get_meeting_name(aiogd_context: Context, **kwargs):
    data = aiogd_context.dialog_data
    return {"meeting_name": data["editing_meeting_id"]}


dialog = Dialog(
    Window(
        Const("Список митингов в этом чате"),
        ScrollingGroup(
            Select(
                Format("{item.name}"),
                id="meetings",
                item_id_getter=lambda x: x.id,
                items="meetings",
                on_click=change_select_meetings,
            ),
            id="meetings_sg",
            width=1,
            height=10,
        ),
        state=SettingsSG.meetings,
        getter=get_meetings
    ),
    Window(
        Format("Настройка {meeting_name}"),
        SwitchTo(
            Const("Подписчики"),
            id="to_participants_ls",
            state=SettingsSG.participants,
        ),
        SwitchTo(
            Const("Расписание"),
            id="to_timetable",
            state=SettingsSG.timetable,
        ),
        state=SettingsSG.meeting_main,
        getter=get_meeting_name
    ),
    Window(
        Const("Подписчики"),
        SwitchTo(
            Const("Назад"),
            id="to_main",
            state=SettingsSG.meeting_main,
        ),
        ScrollingGroup(
            Select(
                Format("{item.is_active_char}{item.display_name}"),
                id="participants",
                item_id_getter=lambda x: x.db_id,
                items="users",
                on_click=change_select_user,
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
                False: Const("Ещё нет запланированного времени"),
                True: Format("Имеющиеся сейчас настройки:\n{timetable}"),
            },
            selector="has_timetable",
        ),
        SwitchTo(
            Const("Добавить время"),
            id="add_time",
            state=SettingsSG.timetable_time,
        ),
        getter=get_timetable,
        state=SettingsSG.timetable,
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
            state=SettingsSG.meeting_main,
        ),
        MessageInput(
            func=get_time,
        ),
        SwitchTo(
            Const("Далее"),
            id="to_timetable_days",
            state=SettingsSG.timetable_days,
            when=lambda data, *args: data["has_data"],
        ),
        getter=get_saved_time,
        state=SettingsSG.timetable_time,
    ),
    Window(
        Const("Выберите дни недели для данного времени"),
        SwitchTo(
            Const("В главное меню"),
            id="to_main",
            state=SettingsSG.meeting_main,
        ),
        Select(
            Format("{item[0]}"),
            id="weekdays",
            item_id_getter=lambda x: x[1],
            items="weekdays",
            on_click=change_weekday,
        ),
        Button(
            Const("Сохранить"),
            id="save_time",
            on_click=save_time,
        ),
        getter=get_weekdays,
        state=SettingsSG.timetable_days,
    )
)
