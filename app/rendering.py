import json

TIME_PATTERN = "%H:%M"
WEEKDAYS = {
    "MON": "ПН",
    "TUE": "ВТ",
    "WED": "СР",
    "THU": "ЧТ",
    "FRI": "ПТ",
    "SUT": "СБ",
    "SUN": "ВС",
}


def render_bool(value: bool) -> str:
    return '✓' if value else '✗'


def render_timetable(data: list[dict[str, str | list[str]]]) -> str:
    return json.dumps(data)


def render_weekdays(days: list[str]) -> list[tuple[str, str]]:
    return [
        (render_bool(en_day in days) + ru_day, en_day) for en_day, ru_day in WEEKDAYS.items()
    ]
