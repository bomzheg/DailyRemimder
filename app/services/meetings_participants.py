from app.dao import HolderDao
from app.models import dto


async def get_available_participants(
        holder_dao: HolderDao, chat: dto.Chat, meeting_id: int
) -> list[dto.Participant]:
    return await holder_dao.get_meeting_participants(chat, meeting_id)


async def turn_participant(
        holder_dao: HolderDao, meeting_id: int, asked_id: int
):
    await holder_dao.meeting.turn_participant(meeting_id, asked_id)
    await holder_dao.commit()
