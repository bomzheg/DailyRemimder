from app.dao import HolderDao
from app.models import dto


users_db = [
    dto.Participant(user_id=666, db_id=1, chat_id=16, display_name="Yuriy", active=False),
    dto.Participant(user_id=42, db_id=2, chat_id=16, display_name="Alexey", active=False),
]


async def get_available_participants(
        holder_dao: HolderDao, chat: dto.Chat, meeting_id: int
) -> list[dto.Participant]:
    return users_db


async def turn_participant(
        holder_dao: HolderDao, chat: dto.Chat, meeting_id: int, asked_id: int
):
    for user in users_db:
        if user.db_id == asked_id:
            user.active = not user.active
