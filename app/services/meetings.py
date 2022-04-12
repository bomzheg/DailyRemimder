from app.dao import HolderDao
from app.models import dto


meetings_db = [
    dto.Meeting(1111, "Утренний стендап", None),
]


async def get_available_meetings(holder_dao: HolderDao, chat: dto.Chat) -> list[dto.Meeting]:
    for meeting in meetings_db:
        meeting.chat = chat
    return meetings_db


async def get_meeting_name_by_id(holder_dao: HolderDao, meeting_id: int) -> str:
    for meeting in meetings_db:
        if meeting.id == meeting_id:
            return meeting.name
    raise RuntimeError(f"unknown meeting id {meeting_id}")
