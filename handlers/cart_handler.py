from aiogram.types import Message, CallbackQuery
from loader import dp, db
from pprint import pprint
from aiogram.dispatcher import FSMContext
from states.user_states import UserState
from handlers.user_handler import send_products_by_category


@dp.message_handler(text='Savatcha 📥', state=UserState.mahsulot_tanlash)
async def cart_handler(xabar: Message, state: FSMContext):
    data = await state.get_data()
    print(
        data
    )




