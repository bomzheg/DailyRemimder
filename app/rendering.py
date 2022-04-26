import json

from app.models.enums import Weekday

TIME_PATTERN = "%H:%M"
WEEKDAYS = {
    Weekday.MON: "ПН",
    Weekday.TUE: "ВТ",
    Weekday.WED: "СР",
    Weekday.THU: "ЧТ",
    Weekday.FRI: "ПТ",
    Weekday.SUT: "СБ",
    Weekday.SUN: "ВС",
}


def render_bool(value: bool) -> str:
    return '✓' if value else '✗'


def render_timetable(data: list[dict[str, str | list[str]]]) -> str:
    # TODO usability render timetable
    return json.dumps(data)


def render_weekdays(days: list[str]) -> list[tuple[str, str]]:
    return [
        (render_bool(en_day in days) + ru_day, en_day.name) for en_day, ru_day in WEEKDAYS.items()
    ]
