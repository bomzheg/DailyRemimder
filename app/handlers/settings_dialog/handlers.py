from datetime import datetime
from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from app.handlers.settings_dialog.states import SettingsSG
from app.models import dto
from app.rendering import TIME_PATTERN
from app.use_cases.meetings import create_new_meeting
from app.use_cases.meetings_participants import turn_participant
from app.use_cases.timetables import add_timetable, get_timetable


async def change_select_user(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer()
    data = manager.data
    await turn_participant(
        data["dao"], manager.current_context().dialog_data["editing_meeting_id"], int(item_id),
    )


async def change_select_time(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer()
    data = manager.current_context().start_data
    if not isinstance(data, dict):
        data = {}
    timetable = await get_timetable(manager.data["dao"], int(item_id))
    data["current_time"] = {"time": timetable.time, "days": list(map(lambda day: day.name, timetable.days))}
    await manager.update(data)
    await manager.switch_to(SettingsSG.timetable_days)


async def change_select_meetings(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer()
    data = manager.current_context().start_data
    if not isinstance(data, dict):
        data = {}
    data["editing_meeting_id"] = int(item_id)
    await manager.update(data)
    await manager.switch_to(SettingsSG.meeting_main)


async def change_weekday(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer()
    data: dict[str, Any] = manager.current_context().dialog_data
    for i, day in enumerate(data["current_time"]["days"]):
        if day == item_id:
            data["current_time"]["days"].pop(i)
            return
    data["current_time"]["days"].append(item_id)


async def save_time(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await c.answer()
    data: dict[str, Any] = dialog_manager.current_context().dialog_data
    new_timetable = data.pop("current_time")
    await add_timetable(dialog_manager.data["dao"], data["editing_meeting_id"], dto.Timetable(**new_timetable))
    await dialog_manager.switch_to(SettingsSG.meeting_main)


async def process_time_message(m: Message, dialog_: Any, manager: DialogManager) -> None:
    try:
        time_ = datetime.strptime(m.text, TIME_PATTERN).time()
    except ValueError:
        await m.answer("Некорректный формат времени. Пожалуйста введите время в формате ЧЧ:ММ")
        return
    data = manager.current_context().start_data
    if not isinstance(data, dict):
        data = {}
    data["current_time"] = {"time": time_.strftime(TIME_PATTERN), "days": []}
    await manager.update(data)
    await manager.switch_to(SettingsSG.timetable_time)


async def process_new_meeting_name(m: Message, dialog_: Any, manager: DialogManager) -> None:
    data = manager.current_context().start_data
    if not isinstance(data, dict):
        data = {}
    data['new_meeting_name'] = m.text
    await manager.update(data)


async def save_new_meeting(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await c.answer()
    data: dict[str, Any] = dialog_manager.current_context().dialog_data
    meeting_name = data.pop('new_meeting_name')
    context_data = dialog_manager.data
    await create_new_meeting(context_data["dao"], meeting_name, context_data["chat"])


async def drop_new_meeting_name(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await c.answer()
    data: dict[str, Any] = dialog_manager.current_context().dialog_data
    data.pop('new_meeting_name', None)
