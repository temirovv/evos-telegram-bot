from aiogram import executor
from handlers import cart_handler, start_handler, user_handler

from loader import dp


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)




'''
data {'sub_location': "Toshkent Olmazor Tumani Beruniy-3 Beruniy shoh ko'chasi 35a", 'category': 'Lavash', 'product_name': "Mol go'shtidan pishloqli lavash", 'count': 7}
data {'sub_location': "Toshkent Olmazor Tumani Beruniy-3 Beruniy shoh ko'chasi 35a", 'category': 'Lavash', 'product_name': "Tovuq go'shtidan qalampir lavash", 'count': 3}
'''
