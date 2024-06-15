import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([f"{item} = ?" for item in parameters])
        return sql, tuple(parameters.values())
    
    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()

        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()

        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_users_table(self):
        sql = """CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER NOT NULL UNIQUE,
        username VARCHAR(255),
        language VARCHAR(10),
        registered_date TEXT
        )"""

        self.execute(sql=sql, commit=True)

    def create_locations_table(self):
        sql = """CREATE TABLE IF NOT EXISTS Locations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        latitude TEXT,
        longitude TEXT,
        location VARCHAR(255),
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
        )"""

        self.execute(sql=sql)

    def create_category_table(self):
        sql = """CREATE TABLE IF NOT EXISTS Category (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(300),
        image TEXT
        )"""
        self.execute(sql, commit=True)

    def create_products_table(self):
        sql = """CREATE TABLE IF NOT EXISTS Products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(300),
        description VARCHAR(3000),
        image TEXT,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES Category(id) ON DELETE CASCADE
        )"""
        self.execute(sql, commit=True)

    def create_orders_table(self):
        '''
        Mahsulotlar uchuz orders yani zakazlar jadvalini yaratish
        '''
        sql = """CREATE TABLE IF NOT EXISTS Orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        order_date TEXT,
        longitude TEXT,
        latitude TEXT,
        location TEXT,
        product_type INTEGER,
        FOREIGN KEY (product_type) REFERENCES ProductTypes(id)
        FOREIGN KEY (user_id) REFERENCES Users(id) ,
        FOREIGN KEY (product_id) REFERENCES Products(id)
        ) """
        self.execute(sql, commit=True)

    def create_product_types_table(self):
        sql = """CREATE TABLE IF NOT EXISTS ProductTypes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_type VARCHAR(200),
        price REAL,
        product_id INTEGER,
        FOREIGN KEY (product_id)  REFERENCES Products(id)
        )"""
        self.execute(sql, commit=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def add_product_type(self, product_type, price, product_name):
        sql = '''INSERT INTO ProductTypes (product_type, price, product_id)
        VALUES (?, ? , (SELECT id FROM Products WHERE name = ?)
        )'''
        self.execute(sql = sql ,parameters=(product_type, price, product_name), commit= True)
    
    def add_products(self, name, image, category_name, description=None):
        sql = """
        INSERT INTO Products (name, image, category_id) VALUES
        (?, ?, (SELECT id FROM Category WHERE name = ?))

        """
        self.execute(sql, parameters=(name, image, category_name), commit=True)
        
    def add_user(self, telegram_id,username,language,registered_date):
        '''bu f-ya nimadur qiladi'''
        sql = """
        INSERT OR IGNORE INTO Users (telegram_id,username,language,registered_date) VALUES
        (?, ?, ?, ?) """
        self.execute(sql=sql,parameters=(telegram_id,username,language,registered_date), commit=True)
    
    # ADD ORDER
    def add_order(self, telegram_id, product_name, quantity, order_date, product_type, longitude, latitude, location = None):
        result = self.check_user_order_exists(telegram_id,product_name, product_type)
        print(f"{result=}")
        if result:
            self.update_user_order(quantity, telegram_id, product_name, product_type)
        else:
            self.add_user_order_if_exists(telegram_id, product_name, quantity, order_date, product_type, longitude, latitude, location)
            

    def add_category(self, category_name: str = '', image_path: str = ''):
        sql = """INSERT INTO Category (name, image) VALUES 
        (?, ?)"""
        self.execute(sql, parameters=(category_name, image_path), commit=True)

    def add_user_location(self, telegram_id, latitude, longitude, location):
        sql=''' INSERT INTO Locations (user_id, latitude, longitude, location) 
        VALUES
        ((SELECT id FROM Users WHERE telegram_id = ?), ?, ?, ?)'''
        self.execute(sql = sql, 
                     parameters=(telegram_id, latitude, longitude, location), 
                     commit = True)

    def add_product_type(self, product_type, price, product_name):
        sql = '''INSERT INTO ProductTypes (product_type, price, product_id)
        VALUES (?, ? , (SELECT id FROM Products WHERE name = ?)
        )'''
        self.execute(sql = sql ,parameters=(product_type, price, product_name), commit= True)

    def add_product_description(self, product_name, description):
        sql = """UPDATE Products SET description = ? WHERE name = ? """
        self.execute(sql, parameters=(description, product_name), commit=True)
    
    def get_order(self, tg_id: int = 0):
        sql = '''SELECT user_id, product_id, quantity, product_type FROM Orders WHERE user_id = (SELECT id FROM Users WHERE telegram_id = ?);
        '''
        return self.execute(sql=sql, parameters=(tg_id,), fetchall=True)

    def get_category_image(self, category_name: str = ''):
        sql = """SELECT image FROM Category WHERE name = ?"""
        data =  self.execute(sql, parameters=(category_name,), fetchone=True)
        if data is not None:
            return data

    def get_product_types(self, product_name):
        sql = '''SELECT id, product_type, price 
        FROM ProductTypes WHERE product_id = (SELECT id FROM Products WHERE name = ?)
        '''
        return self.execute(sql=sql, parameters=(product_name,), fetchall=True)

    def get_product_image(self, product_name):
        sql = """SELECT image FROM Products
        WHERE name = ?"""
        return self.execute(sql, parameters=(product_name,), fetchone=True)
         
    def get_all_category(self):
        sql = """SELECT name FROM Category"""
        data = self.execute(sql, fetchall=True)
        return data

    def get_user_locations(self, telegram_id) -> list:
        sql=""" SELECT location FROM Locations 
        WHERE user_id = (SELECT id FROM Users WHERE telegram_id = ?) """
        return self.execute(sql, parameters=(telegram_id,), fetchall=True)

    def get_products_by_category(self, category_name:str):
        sql = """SELECT name FROM Products 
        WHERE 
        category_id = (SELECT id FROM Category WHERE name = ?)"""   

        data = self.execute(sql=sql, parameters=(category_name,), fetchall=True)   
        return data

    def get_product_description(self, product_name):
        sql = """SELECT description FROM Products
        WHERE name = ?"""
        return self.execute(sql, parameters=(product_name,), fetchone=True)        

    def get_product_name(self, product_id):
        sql = """SELECT name FROM Products WHERE id = ?"""
        return self.execute(sql, parameters=(product_id,), fetchone=True)

    def get_product_price(self, product_type):
        sql = """SELECT price FROM ProductTypes WHERE id = ?"""
        return self.execute(sql, parameters=(product_type,), fetchone=True)

    def update_user_location (self,telegram_id,longitude,latitude):
        sql = """ UPDATE Users SET longitude = ?, latitude = ? WHERE telegram_id =?"""
        self.execute(sql =sql ,parameters= (longitude,latitude,telegram_id),commit=True)
    
    def update_user_order(self, quantity, telegram_id, product_name, product_type):
        sql = '''
                UPDATE Orders SET quantity = ?
                WHERE user_id = (SELECT id FROM Users WHERE telegram_id = ?) AND product_id = (SELECT id FROM Products WHERE name = ?) AND product_type = ?'''
        self.execute(sql, parameters=(quantity, telegram_id, product_name, product_type), commit=True)

    def add_user_order_if_exists(self, telegram_id, product_name, quantity, order_date, product_type, longitude, latitude, location):
        sql = '''
            INSERT INTO Orders (user_id, product_id, quantity, order_date, product_type, longitude, latitude, location) 
            VALUES 
            ((SELECT id FROM Users WHERE telegram_id = ?), (SELECT id FROM Products WHERE name = ?), ?, ?, ?,'''
            
        if location:
            sql += '(SELECT longitude FROM Locations WHERE location = ? LIMIT 1), (SELECT latitude FROM Locations WHERE location = ? LIMIT 1), ?)'
            self.execute(sql=sql, parameters=(telegram_id, product_name, quantity, order_date, product_type, location, location, location), commit=True)
        else:
            sql += '?, ?, ?);'
            self.execute(sql=sql, parameters=(telegram_id, product_name, quantity, order_date, product_type, longitude, latitude, location), commit=True)

    def check_user_order_exists(self, telegram_id, product_name, product_type):
        sql = '''SELECT product_id, product_type FROM Orders WHERE
        user_id = (SELECT id FROM Users WHERE telegram_id = ?) AND product_id = (SELECT id FROM Products WHERE name = ?) AND product_type = ?
        '''
        return self.execute(sql=sql, parameters=(telegram_id, product_name, product_type), fetchone=True)
    
    def clear_user_cart(self, tg_id):
        sql = '''DELETE FROM Orders WHERE 
        user_id = (SELECT id FROM Users WHERE telegram_id = ?)'''
        self.execute(sql, parameters=(tg_id,), commit=True)

    # yangi
    def delete_ordered_product(self, product_id, tg_id):
        sql = '''DELETE FROM Orders WHERE product_id = ? AND user_id = (SELECT id FROM Users WHERE telegram_id = ?);'''
        self.execute(sql, parameters=(product_id, tg_id), commit=True)

def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
