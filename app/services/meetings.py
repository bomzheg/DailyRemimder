from app.dao import HolderDao
from app.models import dto


async def get_available_meetings(holder_dao: HolderDao, chat: dto.Chat) -> list[dto.Meeting]:
    return await holder_dao.meeting.find_all_by_chat(chat.db_id)


async def get_meeting_name_by_id(holder_dao: HolderDao, meeting_id: int) -> str:
    return await holder_dao.meeting.get_by_id(meeting_id)
