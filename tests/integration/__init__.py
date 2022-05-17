import pytest
from alembic.command import upgrade
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db import create_pool
from tests.common import create_app_config
from tests.migrations.test_stairway import alembic_config


@pytest.fixture()
async def session() -> AsyncSession:
    config = create_app_config()
    pool = create_pool(config.db)
    async with pool() as session:
        yield session


@pytest.fixture()
async def set_up_migrations():
    upgrade(alembic_config, "head")
