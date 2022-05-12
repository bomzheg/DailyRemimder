
from app.dao import HolderDao
from app.models import dto


async def load_timetable(holder_dao: HolderDao, meeting_id: int) -> list[dto.Timetable]:
    return await holder_dao.timetable.find_all_by_meeting_id(meeting_id)


async def add_timetable(holder_dao: HolderDao, meeting_id: int, timetable: dto.Timetable):
    await holder_dao.timetable.upsert(meeting_id=meeting_id, timetable=timetable)
    await holder_dao.commit()
