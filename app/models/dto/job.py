from dataclasses import dataclass
from datetime import datetime


@dataclass
class Job:
    meeting_id: int
    name: str
    chat_id: int
    at: datetime
    timetable_id: int
