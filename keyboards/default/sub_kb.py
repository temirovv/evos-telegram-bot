from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


sub_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text='Savatcha 📥')],
        [KeyboardButton(text="⬅️ Ortga")]
    ]
)
