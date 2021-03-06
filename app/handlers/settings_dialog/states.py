from aiogram.dispatcher.fsm.state import StatesGroup, State


class SettingsSG(StatesGroup):
    meetings = State()
    add_meeting = State()
    meeting_main = State()
    participants = State()
    timetable = State()
    timetable_time = State()
    timetable_days = State()
