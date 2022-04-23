from dataclasses import dataclass
from typing import Optional

from app.models import db


@dataclass
class Meeting:
    name: str
    chat_id: int
    id: Optional[int] = None

    @classmethod
    def from_db(cls, other: db.Meeting):
        return cls(
            id=other.id,
            name=other.name,
            chat_id=other.chat_id,
        )

    def to_db(self) -> db.Meeting:
        return db.Meeting(
            name=self.name,
            chat_id=self.chat_id,
        )
