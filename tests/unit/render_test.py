from app.rendering import render_weekdays


def test_render_weekday():
    actual = render_weekdays(["MON", "WED", "THU"])
    expected = [
        ("✓ПН", "MON",),
        ("✗ВТ", "TUE",),
        ("✓СР", "WED",),
        ("✓ЧТ", "THU",),
        ("✗ПТ", "FRI",),
        ("✗СБ", "SAT",),
        ("✗ВС", "SUN",),
    ]
    assert actual == expected
