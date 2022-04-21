from dataclasses import dataclass

from app.models import db


@dataclass
class Meeting:
    id: int
    name: str
    chat_id: int

    @classmethod
    def from_db(cls, other: db.Meeting):
        return cls(
            id=other.id,
            name=other.name,
            chat_id=other.chat_id,
        )
