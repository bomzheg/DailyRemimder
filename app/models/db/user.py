from sqlalchemy import Column, Text, BigInteger, Boolean
from sqlalchemy.orm import relationship

from app.models.db.base import Base
from app.models.db.m2m import meetings_participants, users_chats


class User(Base):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}
    id = Column(BigInteger, primary_key=True)
    tg_id = Column(BigInteger, unique=True)
    first_name = Column(Text, nullable=True)
    last_name = Column(Text, nullable=True)
    username = Column(Text, nullable=True)
    is_bot = Column(Boolean, default=False)
    chats = relationship("Chat", secondary=users_chats, back_populates="users")
    meetings = relationship(
        "Meeting",
        secondary=meetings_participants,
        back_populates="participants",
    )

    def __repr__(self):
        rez = (
            f"<User "
            f"ID={self.tg_id} "
            f"name={self.first_name} {self.last_name} "
        )
        if self.username:
            rez += f"username=@{self.username}"
        return rez + ">"
