from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format


class SettingsSG(StatesGroup):
    main = State()
    participants = State()
    timetable = State()


async def get_participants(c: CallbackQuery, _: Button, manager: DialogManager):
    await c.answer("hello")
    await manager.dialog().switch_to(SettingsSG.participants)


async def change_select():
    pass


dialog = Dialog(
    Window(
        Const("Настройка ежедневного митинга"),
        Button(
            Const("Подписчики"),
            id="participants_ls",
            on_click=get_participants,
        ),
        ScrollingGroup(
            Select(
                Format("{item}"),
                id="participants",
                item_id_getter=lambda x: x.username,
                items="participants",
                on_click=change_select,
            ),
            id="participants_sg",
            width=1,
            height=10,
        ),
        state=SettingsSG.main,
    )
)
