from app.dao import HolderDao
from app.models import dto


async def get_available_meetings(holder_dao: HolderDao, chat: dto.Chat) -> list[dto.Meeting]:
    return await holder_dao.meeting.find_all_by_chat(chat.db_id)


async def create_new_meeting(holder_dao: HolderDao, meeting_name: str, chat: dto.Chat):
    meeting = dto.Meeting(name=meeting_name, chat_id=chat.db_id)
    await holder_dao.meeting.create(meeting)
    await holder_dao.commit()
