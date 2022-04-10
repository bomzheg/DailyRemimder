from sqlalchemy import Table, Column, ForeignKey, Boolean

from app.models.db import Base

meetings_participants = Table(
    "meeting_participants",
    Base.metadata,
    Column("meeting_id", ForeignKey("meetings.id"), primary_key=True),
    Column("participants_id", ForeignKey("users.id"), primary_key=True),
)


users_chats = Table(
    "users_in_chats",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("chat_id", ForeignKey("chats.id"), primary_key=True),
    Column("active", Boolean, default=True)
)
