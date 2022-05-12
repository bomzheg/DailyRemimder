from datetime import time

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dao import BaseDAO
from app.models import dto
from app.models.db import Timetable


class TimetableDAO(BaseDAO[Timetable]):
    def __init__(self, session: AsyncSession):
        super().__init__(Timetable, session)

    async def find_all_by_meeting_id(self, meeting_id: int) -> list[dto.Timetable]:
        result = await self.session.execute(
            select(self.model).where(self.model.meeting_id == meeting_id))
        result_all = result.scalars().all()
        return list(map(dto.Timetable.from_db, result_all))

    async def upsert(self, meeting_id: int, timetable: dto.Timetable):
        try:
            saved = await self._get_by_time(meeting_id=meeting_id, time_=timetable.time)
        except NoResultFound:
            saved = Timetable(meeting_id=meeting_id)
        saved.weekdays = timetable.days
        self.save(saved)
        await self.flush(saved)

    async def _get_by_time(self, meeting_id: int, time_: time) -> Timetable:
        result = await self.session.execute(
            select(self.model).where(
                self.model.meeting_id == meeting_id,
                self.model.time == time_,
            )
        )
        return result.scalar_one()
