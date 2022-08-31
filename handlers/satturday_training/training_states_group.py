from aiogram.dispatcher.filters.state import StatesGroup, State


class Training(StatesGroup):
    fullname = State()
    phone = State()
    children_count = State()
    breakfast = State()
    breakfast_count = State()
