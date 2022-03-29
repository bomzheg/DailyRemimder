import typing

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dao import BaseDAO
from app.models import db, dto


class MeetingDAO(BaseDAO[db.Meeting]):
    def __init__(self, session: AsyncSession):
        super().__init__(db.Meeting, session)

    async def find_by_name(self, name: str, chat_id: int):
        result = await self.session.execute(
            select(self.model).where(
                self.model.name == name,
                self.model.chat_id == chat_id)
        )
        return dto.Meeting.from_db(result.scalar_one())

    async def find_all_by_chat(self, chat_id: int):
        result = await self.session.execute(
            select(self.model).where(self.model.chat_id == chat_id))
        return map(dto.Meeting.from_db, typing.cast(result.all(), list[self.model]))
