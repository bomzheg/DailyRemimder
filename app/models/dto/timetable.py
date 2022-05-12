from __future__ import annotations
from datetime import time

import pydantic

from app.models import db
from app.models.enums import Weekday


class Timetable(pydantic.BaseModel):
    time: time
    days: list[Weekday]
    id: int | None
    meeting_id: int | None

    @classmethod
    def from_db(cls, other: db.Timetable) -> Timetable:
        return cls(
            id=other.id,
            days=other.weekdays,
            time=other.time,
            meeting_id=other.meeting_id,
        )
