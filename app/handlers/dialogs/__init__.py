from aiogram_dialog import DialogRegistry

from app.handlers.dialogs.settings_reminder import dialog


def setup_dialogs(registry: DialogRegistry):
    registry.register(dialog)
