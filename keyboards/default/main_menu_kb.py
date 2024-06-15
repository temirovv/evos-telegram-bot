from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🍴 Menyu")
        ],
        [
            KeyboardButton(text="🛍 Mening buyurtmalarim")
        ],
        [
            KeyboardButton(text="✍️ Fikr bildirish"),
            KeyboardButton(text="⚙️ Sozlamalar")
        ]
    ]
)

menu2nd = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🗺 Mening manzillarim")
        ],
        [
            KeyboardButton(text="📍 Geolokatsiyani yuboring", request_location=True),
            KeyboardButton(text="⬅️ Ortga")
        ],
    ]
)