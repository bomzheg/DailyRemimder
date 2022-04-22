from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, SwitchTo, Button
from aiogram_dialog.widgets.text import Const, Format, Case

from app.handlers.settings_dialog.getters import (
    get_potential_participants,
    get_meetings,
    prepare_weekdays,
    prepare_saved_time,
    prepare_timetable,
    prepare_meeting_name,
)
from app.handlers.settings_dialog.handlers import (
    change_weekday,
    save_time,
    change_select_meetings,
    change_select_user,
    process_time_message,
)
from app.handlers.settings_dialog.states import SettingsSG

dialog = Dialog(
    Window(
        Const("Список митингов в этом чате"),
        SwitchTo(
            Const("Добавить"),
            id="to_add_meeting",
            state=SettingsSG.add_meeting,
        ),
        ScrollingGroup(
            Select(
                Format("{item.name}"),
                id="meetings",
                item_id_getter=lambda x: x.id,
                items="meetings",
                on_click=change_select_meetings,
            ),
            id="meetings_sg",
            width=1,
            height=10,
        ),
        state=SettingsSG.meetings,
        getter=get_meetings
    ),
    Window(
        Format("Настройка {meeting_name}"),
        SwitchTo(
            Const("Подписчики"),
            id="to_participants_ls",
            state=SettingsSG.participants,
        ),
        SwitchTo(
            Const("Расписание"),
            id="to_timetable",
            state=SettingsSG.timetable,
        ),
        state=SettingsSG.meeting_main,
        getter=prepare_meeting_name
    ),
    Window(
        Const("Подписчики"),
        SwitchTo(
            Const("Назад"),
            id="to_main",
            state=SettingsSG.meeting_main,
        ),
        ScrollingGroup(
            Select(
                Format("{item.is_active_char}{item.display_name}"),
                id="participants",
                item_id_getter=lambda x: x.db_id,
                items="users",
                on_click=change_select_user,
            ),
            id="participants_sg",
            width=1,
            height=10,
        ),
        getter=get_potential_participants,
        state=SettingsSG.participants,
    ),
    Window(
        Case(
            {
                False: Const("Ещё нет запланированного времени"),
                True: Format("Имеющиеся сейчас настройки:\n{timetable}"),
            },
            selector="has_timetable",
        ),
        SwitchTo(
            Const("Добавить время"),
            id="add_time",
            state=SettingsSG.timetable_time,
        ),
        getter=prepare_timetable,
        state=SettingsSG.timetable,
    ),
    Window(
        Case(
            {
                False: Const("Введите время в формате ЧЧ:ММ"),
                True: Format(
                    "Будет сохранено: {my_time}. "
                    "Нажмите \"Далее\", если уверены, "
                    "или отправьте другое время в формате ЧЧ:ММ вместо этого"
                ),
            },
            selector="has_data",
        ),
        SwitchTo(
            Const("Назад"),
            id="to_main",
            state=SettingsSG.meeting_main,
        ),
        MessageInput(
            func=process_time_message,
        ),
        SwitchTo(
            Const("Далее"),
            id="to_timetable_days",
            state=SettingsSG.timetable_days,
            when=lambda data, *args: data["has_data"],
        ),
        getter=prepare_saved_time,
        state=SettingsSG.timetable_time,
    ),
    Window(
        Const("Выберите дни недели для данного времени"),
        SwitchTo(
            Const("В главное меню"),
            id="to_main",
            state=SettingsSG.meeting_main,
        ),
        Select(
            Format("{item[0]}"),
            id="weekdays",
            item_id_getter=lambda x: x[1],
            items="weekdays",
            on_click=change_weekday,
        ),
        Button(
            Const("Сохранить"),
            id="save_time",
            on_click=save_time,
        ),
        getter=prepare_weekdays,
        state=SettingsSG.timetable_days,
    )
)
