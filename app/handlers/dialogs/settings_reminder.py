from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Group, Button
from aiogram_dialog.widgets.text import Const


class SettingsSG(StatesGroup):
    main = State()
    participants = State()
    timetable = State()


async def get_participants(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.answer("hello")


dialog = Dialog(
    Window(
        Const("Настройка ежедневного митинга"),
        Group(
            Button(
                Const("Подписчики"),
                id="participants_ls",
                on_click=get_participants,
            ),
        ),
        state=SettingsSG.main,
    )
)
