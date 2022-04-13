from typing import Any

from aiogram_dialog import DialogManager
from aiogram_dialog.context.context import Context

from app.dao import HolderDao
from app.models import dto
from app.rendering import render_timetable, render_weekdays
from app.services.meetings import get_available_meetings
from app.services.meetings_participants import get_available_participants


async def get_potential_participants(dao: HolderDao, chat: dto.Chat, dialog_manager: DialogManager, **kwargs):
    return {"users": (await get_available_participants(
        dao, chat, dialog_manager.current_context().dialog_data["editing_meeting_id"]
    ))}


async def get_meetings(dao: HolderDao, chat: dto.Chat, **kwargs):
    return {"meetings": await get_available_meetings(dao, chat)}


async def prepare_weekdays(dialog_manager: DialogManager, **kwargs):
    data: dict[str, Any] = dialog_manager.current_context().dialog_data
    days: list[str] = data["new_time"]["days"]
    return {"weekdays": render_weekdays(days)}


async def prepare_saved_time(dialog_manager: DialogManager, **kwargs):
    data: dict[str, Any] = dialog_manager.current_context().dialog_data
    my_time = data.get("new_time", {}).get("time", None)
    return {
        "my_time": my_time if my_time else "None",
        "has_data": bool(my_time),
    }


async def prepare_timetable(dialog_manager: DialogManager, **kwargs):
    data: dict[str, Any] = dialog_manager.current_context().dialog_data
    timetable = data.get("timetable", [])
    return {
        "timetable": render_timetable(timetable),
        "has_timetable": bool(timetable),
    }


async def prepare_meeting_name(aiogd_context: Context, **kwargs):
    data = aiogd_context.dialog_data
    return {"meeting_name": data["editing_meeting_id"]}
