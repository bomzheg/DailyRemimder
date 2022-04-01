from sqlalchemy import Table, Column, ForeignKey

from app.models.db import Base

meetings_participants = Table(
    "meeting_participants",
    Base.metadata,
    Column("meeting_id", ForeignKey("meetings.id"), primary_key=True),
    Column("participants_id", ForeignKey("users.id"), primary_key=True),
)
