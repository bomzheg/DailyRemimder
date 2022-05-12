from sqlalchemy import delete, func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, TypeVar, Type, Generic

from sqlalchemy.orm import joinedload

from app.models import dto, db

from app.models.db.base import Base


Model = TypeVar('Model', Base, Base)


class BaseDAO(Generic[Model]):
    def __init__(self, model: Type[Model], session: AsyncSession):
        self.model = model
        self.session = session

    async def _get_all(self) -> List[Model]:
        result = await self.session.execute(select(self.model))
        return result.all()

    async def _get_by_id(self, id_: int) -> Model:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id_)
        )
        return result.scalar_one()

    def _save(self, obj: Model):
        self.session.add(obj)

    async def delete_all(self):
        await self.session.execute(
            delete(self.model)
        )

    async def count(self):
        result = await self.session.execute(
            select(func.count(self.model.id))
        )
        return result.scalar_one()

    async def commit(self):
        await self.session.commit()

    async def flush(self, *objects):
        await self.session.flush(objects)

    # ------------some concrete but common methods--------------:

    async def _get_chat_loaded_participants(self, chat: dto.Chat) -> db.Chat:
        chat_db: db.Chat = await self.session.get(
            db.Chat, chat.db_id, options=[joinedload(db.Chat.users)],
        )
        return chat_db
