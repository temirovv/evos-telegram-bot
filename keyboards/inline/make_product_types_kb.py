from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import db


def make_products_inline(product_name: str):
    result = db.get_product_types(product_name)
    menu = InlineKeyboardMarkup()
    tugmamalar = []

    for line in result:
        product_id, product_type, price = line
        print(f"{product_type} -- {price} sum")
        tugmamalar.append(
            InlineKeyboardButton(text=f"{product_type} - {int(price)}", callback_data=f'{product_id}:{product_name}:{product_type}:{price}')
        )

    menu.add(*tugmamalar)
    return menu
    
