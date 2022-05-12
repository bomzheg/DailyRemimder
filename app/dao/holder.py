from dataclasses import dataclass, field

from sqlalchemy.ext.asyncio import AsyncSession

from app.dao import UserDAO, ChatDAO
from app.dao.meeting import MeetingDAO
from app.dao.timetable import TimetableDAO
from app.models import dto


@dataclass
class HolderDao:
    session: AsyncSession
    user: UserDAO = field(init=False)
    chat: ChatDAO = field(init=False)
    meeting: MeetingDAO = field(init=False)
    timetable: TimetableDAO = field(init=False)

    def __post_init__(self):
        self.user = UserDAO(self.session)
        self.chat = ChatDAO(self.session)
        self.meeting = MeetingDAO(self.session)
        self.timetable = TimetableDAO(self.session)

    async def commit(self):
        await self.session.commit()

    async def get_meeting_participants(self, chat: dto.Chat, meeting_id: int) -> list[dto.Participant]:
        users = await self.user.get_chat_participants(chat)
        meeting = await self.meeting.get_by_id_load_participants(meeting_id)
        return [
            dto.Participant(
                user_id=user.tg_id,
                db_id=user.id,
                chat_id=chat.tg_id,
                display_name=user.fullname,
                active=user in meeting.participants,
            ) for user in users
        ]

