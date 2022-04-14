import typing

from app.dao import HolderDao

Timetable: typing.TypeAlias = dict[str, list[str]]
"""{"time": "11:30", "days": ["WED", "THU", "FRI"]}"""


async def load_timetable(holder_dao: HolderDao, meeting_id: int) -> list[Timetable]:
    pass


async def add_timetable(holder_dao: HolderDao, meeting_id: int, timetable: Timetable):
    pass
