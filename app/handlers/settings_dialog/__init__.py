from aiogram_dialog import DialogRegistry

from app.handlers.settings_dialog.dialogs import dialog


def setup_dialogs(registry: DialogRegistry):
    registry.register(dialog)
