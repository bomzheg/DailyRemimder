import typing

from app.dao import HolderDao

Timetable: typing.TypeAlias = list[dict[str, list[str]]]


async def load_timetable(holder_dao: HolderDao, meeting_id: int) -> Timetable:
    pass


async def add_timetable(holder_dao: HolderDao, meeting_id: int, timetable: Timetable):
    pass
