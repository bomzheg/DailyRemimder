from typing import Any

from aiogram_dialog import DialogManager
from aiogram_dialog.context.context import Context

from app.dao import HolderDao
from app.models import dto
from app.rendering import render_weekdays
from app.services.meetings import get_available_meetings, get_meeting_by_id
from app.services.meetings_participants import get_available_participants
from app.services.timetables import load_timetable


async def get_potential_participants(dao: HolderDao, chat: dto.Chat, dialog_manager: DialogManager, **kwargs):
    return {"users": (await get_available_participants(
        dao, chat, dialog_manager.current_context().dialog_data["editing_meeting_id"]
    ))}


async def get_meetings(dao: HolderDao, chat: dto.Chat, **kwargs):
    return {"meetings": await get_available_meetings(dao, chat)}


async def prepare_weekdays(dialog_manager: DialogManager, **kwargs):
    data: dict[str, Any] = dialog_manager.current_context().dialog_data
    days: list[str] = data["current_time"]["days"]
    return {
        "weekdays": render_weekdays(days),
        "current_time": data["current_time"]["time"],
    }


async def prepare_saved_time(dialog_manager: DialogManager, **kwargs):
    data: dict[str, Any] = dialog_manager.current_context().dialog_data
    my_time = data.get("current_time", {}).get("time", None)
    return {
        "my_time": my_time if my_time else "None",
        "has_data": bool(my_time),
    }


async def prepare_timetable(dao: HolderDao, dialog_manager: DialogManager, **kwargs):
    data: dict[str, Any] = dialog_manager.current_context().dialog_data
    timetable = await load_timetable(dao, data["editing_meeting_id"])
    return {
        "timetable": timetable,
        "has_timetable": bool(timetable),
    }


async def prepare_meeting_name(dao: HolderDao, aiogd_context: Context, **kwargs):
    data = aiogd_context.dialog_data
    return {"meeting_name": await get_meeting_by_id(dao, data["editing_meeting_id"])}


async def get_saved_date(aiogd_context: Context, **kwargs):
    data = aiogd_context.dialog_data
    meeting_name = data.get("new_meeting_name", None)
    return {
        "new_meeting_name": meeting_name,
        "has_data": bool(meeting_name),
    }
