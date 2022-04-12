from __future__ import annotations
from dataclasses import dataclass

from app.rendering import render_bool


@dataclass
class Participant:
    db_id: int
    user_id: int
    chat_id: int
    active: bool
    display_name: str

    @property
    def is_active_char(self) -> str:
        return render_bool(self.active)
