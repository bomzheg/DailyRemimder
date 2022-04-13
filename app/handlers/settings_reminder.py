from aiogram import Dispatcher
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from app.handlers.settings_dialog.states import SettingsSG


async def start_setup(_: Message, dialog_manager: DialogManager):
    await dialog_manager.start(SettingsSG.meetings, mode=StartMode.RESET_STACK)


def setup_settings(dp: Dispatcher):
    dp.message.register(start_setup, commands="settings")
