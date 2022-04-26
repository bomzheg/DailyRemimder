from sqlalchemy.ext.asyncio import AsyncSession

from app.dao import BaseDAO
from app.models.db import Timetable


class TimetableDAO(BaseDAO[Timetable]):
    def __init__(self, session: AsyncSession):
        super().__init__(Timetable, session)
