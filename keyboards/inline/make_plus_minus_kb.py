from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def make_plus_minus_kb(count=1):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='-', callback_data='product_minus'),
                InlineKeyboardButton(text=f"{count}", callback_data='count'),
                InlineKeyboardButton(text='+', callback_data='product_plus')
            ],
            [
                InlineKeyboardButton(text='📥 Savatga qo\'shish', callback_data='add_to_cart')
            ]
        ]
    )
