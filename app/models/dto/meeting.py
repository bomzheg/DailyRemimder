from dataclasses import dataclass

from app.models import dto, db


@dataclass
class Meeting:
    id: int
    name: str
    chat: dto.Chat

    @classmethod
    def from_db(cls, other: db.Meeting):
        return cls(
            id=other.id,
            name=other.name,
            chat=dto.Chat.from_db(other.chat),
        )
