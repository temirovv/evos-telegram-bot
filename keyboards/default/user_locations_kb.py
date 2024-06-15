from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import db


# 2 xil ma'lumot turini olishi mumkin bo'lgan parametr
def make_locations_kb(telegram_id: str | int):
    lokatsiyalar = db.get_user_locations(telegram_id)
    print(
        f"{lokatsiyalar=}"
    )
    menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    for matn in lokatsiyalar:
        button = KeyboardButton(text=matn[0])

        menu.add(button)

    menu.add(
        KeyboardButton(text="⬅️ Ortga")
    )
    return menu
