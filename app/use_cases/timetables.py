from app.dao import HolderDao
from app.models import dto


async def load_timetable(holder_dao: HolderDao, meeting_id: int) -> list[dto.Timetable]:
    return await holder_dao.timetable.find_all_by_meeting_id(meeting_id)


async def get_timetable(holder_dao: HolderDao, timetable_id: int) -> dto.Timetable:
    return await holder_dao.timetable.get_by_id(timetable_id)


async def add_timetable(holder_dao: HolderDao, meeting_id: int, timetable: dto.Timetable):
    await holder_dao.timetable.upsert(meeting_id=meeting_id, timetable=timetable)
    await holder_dao.commit()


async def get_jobs(holder_dao: HolderDao, date_range: dto.DatetimeRange, limit: int) -> list[dto.Job]:
    return await holder_dao.timetable.get_jobs_in_range(date_range=date_range, limit=limit)
