from dataclasses import dataclass
from datetime import time

from app.models.enums import Weekday


@dataclass
class Timetable:
    time: time
    weekdays: list[Weekday]
