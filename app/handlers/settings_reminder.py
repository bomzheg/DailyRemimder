from aiogram import Dispatcher
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from app.handlers.dialogs.settings_reminder import SettingsSG


async def start_setup(_: Message, dialog_manager: DialogManager):
    await dialog_manager.start(SettingsSG.main, mode=StartMode.RESET_STACK)


def setup_settings(dp: Dispatcher):
    dp.message.register(start_setup, commands="settings")
