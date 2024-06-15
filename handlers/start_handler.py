from aiogram.types import Message
from loader import dp, db
from pprint import pprint
from aiogram.dispatcher import FSMContext

from keyboards.default.main_menu_kb import menu, menu2nd
from states.user_states import UserState


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: Message):
    pprint(
        dict(message)
    )
    await message.reply("Hellu! dear", reply_markup=menu)
    
    telegram_id = message.from_user.id
    username = message.from_user.username
    language = message.from_user.language_code
    registered_date = message.date

    db.add_user(
        telegram_id,
        username,
        language,
        registered_date
    )


@dp.message_handler(text="🍴 Menyu")
async def handle_menu(message: Message):
    await UserState.location.set()
    await message.answer('yana bitta Hellu! dear', reply_markup=menu2nd)


