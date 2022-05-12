from app.dictionaries import WEEKDAYS

TIME_PATTERN = "%H:%M"


def render_bool(value: bool) -> str:
    return '✓' if value else '✗'


def render_weekdays(days: list[str]) -> list[tuple[str, str]]:
    return [
        (render_bool(en_day.name in days) + ru_day, en_day.name) for en_day, ru_day in WEEKDAYS.items()
    ]
