from aiogram.dispatcher.filters.state import StatesGroup, State


class Training(StatesGroup):
    fullname = State()
    phone = State()
    breakfast = State()
    breakfast_count = State()
