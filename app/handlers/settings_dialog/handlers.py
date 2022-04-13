from datetime import datetime
from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from app.handlers.settings_dialog.states import SettingsSG
from app.rendering import TIME_PATTERN
from app.services.meetings_participants import turn_participant


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


async def change_weekday(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer()
    data: dict[str, Any] = manager.current_context().dialog_data
    for i, day in enumerate(data["new_time"]["days"]):
        if day == item_id:
            data["new_time"]["days"].pop(i)
            return
    data["new_time"]["days"].append(item_id)


async def save_time(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await c.answer()
    data: dict[str, Any] = dialog_manager.current_context().dialog_data
    timetable = data.setdefault("timetable", [])
    timetable.append(data.pop("new_time"))
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
    data['new_time'] = {"time": time_.strftime(TIME_PATTERN), "days": []}
    await manager.update(data)
    await manager.switch_to(SettingsSG.timetable_time)
