import typing

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

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

    async def get_by_id_load_participants(self, id_: int) -> db.Meeting:
        result = await self.session.get(
            self.model,
            id_,
            options=[joinedload(db.Meeting.participants)],
        )
        return result.scalar_one()

    async def turn_participant(self, meeting_id: int, user_id: int):
        meeting = await self.get_by_id(meeting_id)
        user_res = await self.session.get(
            db.User,
            user_id,
            options=[joinedload(db.User.meetings)]
        )
        user: db.User = user_res.scalar_one()
        if meeting in user.meetings:
            user.meetings.remove(meeting)
        else:
            user.meetings.append(meeting)
