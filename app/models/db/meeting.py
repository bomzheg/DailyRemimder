from sqlalchemy import Column, Text, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from app.models.db.base import Base


class Meeting(Base):
    __tablename__ = "meetings"
    __mapper_args__ = {"eager_defaults": True}
    id = Column(BigInteger, primary_key=True)
    name = Column(Text, nullable=True)
    chat_id = Column(BigInteger, ForeignKey("chats.id"))
    chat = relationship("Chat", back_populates="meetings")
    timetables = relationship("Timetable", back_populates="meeting")
