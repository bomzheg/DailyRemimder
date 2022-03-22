from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format
from typing import Any

from dataclasses import dataclass


class SettingsSG(StatesGroup):
    main = State()
    participants = State()
    timetable = State()


@dataclass
class Participant:
    tg_id: int
    db_id: int
    username: str
    name: str
    checked: bool = False

    @property
    def is_checked(self):
        return '✓' if self.checked else ''


users_db = {"users": [
    Participant(tg_id=666, db_id=1, username="bomzheg", name="Yuriy"),
    Participant(tg_id=42, db_id=2, username="alex", name="Alexey"),
]}


async def get_participants(c: CallbackQuery, _: Button, manager: DialogManager):
    await c.answer()
    await manager.dialog().switch_to(SettingsSG.participants)


async def change_select(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer(f"clicked {item_id}")
    asked_id = int(item_id)
    for user in users_db["users"]:
        if user.tg_id == asked_id:
            user.checked = not user.checked


async def get_potential_participants(dialog_manager: DialogManager, **kwargs):
    return users_db


dialog = Dialog(
    Window(
        Const("Настройка ежедневного митинга"),
        Button(
            Const("Подписчики"),
            id="participants_ls",
            on_click=get_participants,
        ),
        state=SettingsSG.main,
    ),
    Window(
        Const("Подписчики"),
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
)
