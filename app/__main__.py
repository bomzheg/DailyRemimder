import logging
from pathlib import Path

from aiogram import Dispatcher, Bot
from aiogram.dispatcher.filters import ContentTypesFilter
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram_dialog import DialogRegistry

from app.config import load_config
from app.config.logging_config import setup_logging
from app.handlers import setup_handlers
from app.handlers.settings_dialog import setup_dialogs
from app.middlewares import setup_middlewares
from app.models.config.main import Paths
from app.models.db import create_pool

logger = logging.getLogger(__name__)


def main():
    paths = Paths(Path(__file__).parent.parent)  # TODO get this dir from env

    setup_logging(paths)
    config = load_config(paths)

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    registry = DialogRegistry(dp)
    setup_dialogs(registry)
    dp.message.bind_filter(ContentTypesFilter)
    setup_middlewares(dp, create_pool(config.db), config.bot)
    setup_handlers(dp, config.bot)

    bot = Bot(config.bot.token, parse_mode="HTML")

    logger.info("started")
    dp.run_polling(bot)


if __name__ == '__main__':
    main()
