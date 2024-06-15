from aiogram.types import Message, ContentTypes, InputFile, CallbackQuery
from pprint import pprint
from loader import dp, db
from utils.utils import get_location_name
from aiogram.dispatcher import FSMContext
from states.user_states import UserState

from keyboards.default import menu2nd, menu, make_locations_kb, make_categories_kb, make_products_kb
from keyboards.inline.make_product_types_kb import make_products_inline
from keyboards.inline.make_plus_minus_kb import make_plus_minus_kb
from keyboards.default.sub_kb import sub_menu
from keyboards.inline.cart_inline_kb import cart_inline_products


@dp.message_handler(text="⬅️ Ortga", state=UserState.location)
async def go_back(xabar: Message, state: FSMContext):
    await xabar.answer(text="Quyidagilardan birini tanlang", reply_markup=menu)
    await state.finish()


@dp.message_handler(text="⬅️ Ortga", state=UserState.sub_location)
async def go_back(xabar: Message, state: FSMContext):
    await xabar.answer(text="Quyidagilardan birini tanlang", reply_markup=menu2nd)
    await UserState.location.set()


@dp.message_handler(text="⬅️ Ortga", state=UserState.product_selection)
async def go_back(xabar: Message, state: FSMContext):
    await xabar.answer(text="Quyidagilardan birini tanlang", reply_markup=make_categories_kb())
    await UserState.location.set()


@dp.message_handler(text="⬅️ Ortga", state=UserState.mahsulot_tanlash)
async def go_back(xabar: Message, state: FSMContext):
    data = await state.get_data()
    category = data.get('category', 'Lavash')
    await xabar.answer(text="Quyidagilardan birini tanlang", 
                       reply_markup=make_products_kb(category))
    await UserState.product_selection.set()


@dp.message_handler(text='📥 Savat', state=UserState.mahsulot_tanlash)
async def cart_send_handler(xabar: Message, state: FSMContext):
    tg_id = xabar.from_user.id
    menu, text = cart_inline_products(tg_id)
    await xabar.answer(text=text, reply_markup=menu)


@dp.callback_query_handler(text='add_to_cart', state=UserState.mahsulot_tanlash)
async def add_to_cart(call: CallbackQuery, state = FSMContext):
    print('add to cart ishladi')
    data = await state.get_data()
    
    
    product_name = data.get('product_name')
    quantity = data.get('count')
    tg_id = call.from_user.id
    longitude = data.get('longitude')
    latitude = data.get('latitude')
    location = data.get('sub_location', None)
    product_id = data.get('product_id')
    order_date = call.message.date

    db.add_order(
        telegram_id=tg_id,
        product_name=product_name,
        quantity=quantity,
        order_date=order_date,
        product_type=product_id,
        longitude=longitude,
        latitude=latitude,
        location=location
    )

    await state.update_data(
        {'cart_exists': True}
    )

    await UserState.product_selection.set()
    message = await call.message.edit_reply_markup()
    message.text = data.get('category')
    await send_products_by_category(message, state)
    print('data', data)


@dp.callback_query_handler(lambda call: call.data.startswith('cancel'), state=UserState.mahsulot_tanlash)
async def cancel_ordered_product_handler(call: CallbackQuery, state: FSMContext):
    _ , product_id, product_name = call.data.split('.')
    tg_id = call.from_user.id

    db.delete_ordered_product(product_id, tg_id)
    menu, text = cart_inline_products(tg_id)

    await call.message.edit_text(text)
    await call.message.edit_reply_markup(
        menu
    )

    await call.answer(f'{product_name} o\'chirildi', cache_time=60)


@dp.message_handler(content_types=['location'], state=UserState.location)
async def location_handler(xabar: Message, state: FSMContext):    
    # print(f"{xabar.set_current=}")
    print('location handler degan funksiyam ishladi')
    latitude = xabar.location.latitude
    longitude = xabar.location.longitude
    adris = get_location_name(latitude, longitude)
    
    house_number = adris.get('house_number', '')
    road = adris.get('road', '')
    county = adris.get('county', '')
    city = adris.get('city', '')
    residental = adris.get('residential', '')

    location = f"{city} {county} {residental} {road} {house_number}".strip()
    telegram_id = xabar.from_user.id

    db.add_user_location(
        telegram_id,
        latitude,
        longitude,
        location
    )


    await state.update_data(
        {'latitude': latitude, 
         'longitude': longitude, 
         'location': location}
    )
    await UserState.product_selection.set()
    await xabar.answer('Quyidagilardan birini tanlang! :)', reply_markup=make_categories_kb())

    print(
        location
    )
    print(adris)
    print("__________________________--")


@dp.message_handler(text="🗺 Mening manzillarim", state=UserState.location)
async def send_user_locations(xabar: Message):
    telegram_id = xabar.from_user.id

    await UserState.sub_location.set()
    await xabar.answer(
        text="Yetkazib berish manzilni tanlang", 
        reply_markup=make_locations_kb(telegram_id))


@dp.message_handler(state=UserState.sub_location)
async def bu_prosta_funksiya_nomi(kotta_xabar: Message, state: FSMContext):
    textcha = kotta_xabar.text
    await state.update_data(
        {'sub_location': textcha}
    ) 
    await UserState.product_selection.set()
    await kotta_xabar.answer(
        'Quyidagilardan birini tanlang!',
        reply_markup=make_categories_kb())


@dp.message_handler(state=UserState.product_selection)
async def send_products_by_category(xabar: Message, state: FSMContext):
    text = xabar.text
    data = await state.get_data()
    cart_exists = data.get('cart_exists', False)

    await xabar.answer(text="Mahsulotni tanlang!", 
                       reply_markup=make_products_kb(text, cart_exists))
    
    data = db.get_category_image(category_name=text)
    if data is None:
        await xabar.answer('iltimos quyidagi tugmalardan birini tanlang!')
        return

    image = data[0]
    photo = InputFile(path_or_bytesio=image)
    await xabar.answer_photo(photo)
    await state.update_data(
        {'category': text}
    )
    await UserState.mahsulot_tanlash.set()


@dp.message_handler(state=UserState.mahsulot_tanlash)
async def mahsulot_tanla(xabar: Message, state: FSMContext):
    text = xabar.text
    image = db.get_product_image(product_name=text)
    description = db.get_product_description(text)

    if image is None:
        await xabar.answer('iltimos quyidagi tugmalardan birini tanlang!')
        return
    else:
        await xabar.answer('Quyidagilardan birini tanlang', reply_markup=sub_menu)      
    if description is None:
        description = '_'
    else:
        description = description[0]
    
    await state.update_data(
        {
            'product_name': text,
            'count': 1
        }
    )
    photo = InputFile(path_or_bytesio=image[0])
    await xabar.answer_photo(photo, caption=description, reply_markup=make_products_inline(text))


@dp.callback_query_handler(text='product_plus' ,state=UserState.mahsulot_tanlash)
async def mahsulot_callback_query_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    count = data.get('count', 1)
    count += 1
    await call.message.edit_reply_markup(make_plus_minus_kb(count))
    await state.update_data(
        {
            'count': count
        }
    )
    await call.answer(text=f'{count} ta')
    print('plus bosildi')

    
@dp.callback_query_handler(text = 'product_minus', state=UserState.mahsulot_tanlash)
async def mahsulot_callback_query_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    count = data.get('count', 1)
    if count == 1:
        return
    
    count = count if not count > 1 else count - 1
    
    await call.message.edit_reply_markup(make_plus_minus_kb(count))
    await state.update_data(
        {
            'count': count
        }
    )  
    await call.answer(text=f'{count} ta')
    print('minus bosildi')
    

@dp.callback_query_handler(text = 'clear_cart', state=UserState.mahsulot_tanlash)
async def clear_user_cart_handler(call: CallbackQuery, state: FSMContext):
    tg_id = call.from_user.id
    db.clear_user_cart(tg_id)
    
    await state.update_data({'cart_exists': False})

    await call.answer('Savatchangiz tozalandi!')
    await call.message.answer('Bo\'limni tanlang', reply_markup=make_categories_kb())
    await UserState.product_selection.set()
    await call.message.delete()
    


@dp.callback_query_handler(state=UserState.mahsulot_tanlash)
async def mahsulot_callback_query_handler(call: CallbackQuery, state: FSMContext):
    call_text = call.data
    product_id, product_name, product_type, price = call_text.split(':')
    await state.update_data(
        {'product_id': product_id}
    )
    await state.update_data('')
    print(f'{call_text=}')

    await call.message.edit_reply_markup(make_plus_minus_kb())
    
