from aiogram.utils.text_decorations import HtmlDecoration

from app.models.dto.timetable import WEEKDAYS

TIME_PATTERN = "%H:%M"


def render_bool(value: bool) -> str:
    return '✓' if value else '✗'


def render_timetable(data: list['dto.Timetable']) -> str:
    # TODO usability render timetable
    return HtmlDecoration().quote(str(data))


def render_weekdays(days: list[str]) -> list[tuple[str, str]]:
    return [
        (render_bool(en_day in days) + ru_day, en_day.name) for en_day, ru_day in WEEKDAYS.items()
    ]
