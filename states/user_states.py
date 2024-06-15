from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    location = State()
    sub_location = State()
    product_selection = State()
    mahsulot_tanlash = State()
