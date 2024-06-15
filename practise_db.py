from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from database.db_sqlite import Database
from pprint import pprint

baza = Database(path_to_db="main.sqlite3")




# import sqlite3
# con = sqlite3.connect('main.sqlite3')
# cur = con.cursor()


# sl = '''DROP TABLE Orders;'''
# cur.execute(sl)
# con.commit()
# con.close()


# result = baza.check_user_order_exists(10518730773, 3, 14)
# print(result)
# baza.create_category_table()
# baza.create_users_table()
# baza.create_products_table()
# baza.create_orders_table()
# baza.create_product_types_table()
# baza.create_locations_table()

# baza.create_product_types_table()

# baza.add_category('Lavash', 'images/categories/Lavash.jpg')
# baza.add_category('Trindwich', 'images/categories/Trindwich.jpg')
# baza.add_category('Shaurma', 'images/categories/shaurma.jpg')
# baza.add_category('Burger', 'images/categories/burger.jpg')
# baza.add_category('Sub', 'images/categories/sub.jpg')
# baza.add_category('Kartoshka', 'images/categories/kartoshka4.jpg')
# baza.add_category('Hot Dog', 'images/categories/hot-dog.jpg')
# baza.add_category('Sneklar', 'images/categories/senki.jpg')
# baza.add_category('Salat, garnir, non', 'images/categories/salad.jpg')
# baza.add_category('Souslar', 'images/categories/sause.jpg')
# baza.add_category('Setlar', 'images/categories/sets.jpg')
# baza.add_category('Desertlar', 'images/categories/desserts.jpg')
# baza.add_category('Issiq ichimliklar', 'images/categories/hot drinks.jpg')
# baza.add_category('Sovuq ichimliklar', 'images/categories/cold drinks.jpg')
# baza.add_category('Combo', 'images/categories/combo.jpg')

# baza.add_products("Tovuq go`shtidan lavash", 'images/lavash/Tovuq goshtidan lavash.jpg','Lavash',)
# baza.add_products("Mol go'shtidan pishloqli lavash", 'images/lavash/Mol goshtidan pishloqli lavash.jpg','Lavash',)
# baza.add_products("Mol go'shtidan qalampir lavash", 'images/lavash/Mol goshtidan qalampir lavash.jpg','Lavash',)
# baza.add_products("Tovuq go'shtidan qalampir lavash", 'images/lavash/Tovuq goshtidan qalampir lavash.jpg.','Lavash',)
# baza.add_products("Tovuq go`shtidan pishloqli lavash", 'images/lavash/Tovuq goshtidan pishloqli lavash.jpg','Lavash',)
# baza.add_products("Fitter", 'images/lavash/Fitter.jpg','Lavash',)
# baza.add_products("Mol go`shtidan lavash", 'images/lavash/Mol goshtidan lavash.jpg',category_name='Lavash',)



# baza.add_product_type('Mini', 25000, "Tovuq go`shtidan pishloqli lavash")
# baza.add_product_type('Big', 35000, "Tovuq go`shtidan pishloqli lavash")

# baza.add_product_type('Mini', 20000, "Tovuq go'shtidan qalampir lavash")
# baza.add_product_type('Big', 30000, "Tovuq go'shtidan qalampir lavash")

# baza.add_product_type('Mini', 20000, "Mol go'shtidan qalampir lavash")
# baza.add_product_type('Big', 20000, "Mol go'shtidan qalampir lavash")

# baza.add_product_type('Mini', 24000, "Mol go'shtidan pishloqli lavash")
# baza.add_product_type('Big', 36000, "Mol go'shtidan pishloqli lavash")

# baza.add_product_description("Mol go'shtidan pishloqli lavash", "mol go'shti bo'lakchalaridan ajoyib lavash, yeganingizda yengil tamni xis qiling va ushbu taomdan rohatlaning")
# result = baza.get_product_types(product_name="Mol go'shtidan pishloqli lavash")

# data = baza.get_products_by_categories(category_name='Lavash')
# pprint(data)

# def sort_user_products(tg_id: int):
#     data = baza.get_order(tg_id)
#     for user_id, product_id, quantity in data:
#         print(
#             f"{user_id=}"
#         )
#         print(
#             f"product name: {baza.get_product_name(product_id)[0]}"
#         )
#         print(
#             f"{quantity=}"
#         )

# sort_user_products(1058730773)
