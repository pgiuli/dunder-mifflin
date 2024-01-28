import sqlite3

def create_db():
    conn = sqlite3.connect('database.db')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS Stock (
            ItemID TEXT NOT NULL,
            CurrentStock INTEGER NOT NULL,
            MaxStock INTEGER NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS Exchange (
            DisplayName TEXT NOT NULL,
            ItemID TEXT NOT NULL,
            ChangeCount INTEGER NOT NULL,
            BuyPrice REAL NOT NULL,
            SellPrice REAL NOT NULL,
            MinSellAmount REAL NOT NULL,
            FOREIGN KEY(ItemID) REFERENCES Stock(ItemID)
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS Discount (
            ItemID TEXT NOT NULL,
            BuyDiscount REAL NOT NULL,
            SellDiscount REAL NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS Stats (
            ItemID TEXT NOT NULL,
            Operation TEXT NOT NULL,
            Amount INTEGER NOT NULL,
            Area INTEGER NOT NULL,
            FOREIGN KEY(ItemID) REFERENCES Stock(ItemID)
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            UserID TEXT PRIMARY KEY,
            DisplayName TEXT NOT NULL,
            Role TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id, display_name, role):
    conn = sqlite3.connect('database.db')
    conn.execute('''
        INSERT INTO Users (UserID, DisplayName, Role)
        VALUES (?, ?, ?)
    ''', (user_id, display_name, role))
    conn.commit()
    conn.close()

def get_user_displayname_and_role(user_id): # Returns tuple (display_name, role)
    conn = sqlite3.connect('database.db')
    cursor = conn.execute('''
        SELECT DisplayName, Role
        FROM Users
        WHERE UserID = ?
    ''', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def get_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.execute('''
        SELECT UserID, DisplayName, Role
        FROM Users
    ''')
    result = cursor.fetchall()
    conn.close()
    return result

def add_item(item_id, current_stock, max_stock):
    conn = sqlite3.connect('database.db')
    conn.execute('''
        INSERT INTO Stock (ItemID, CurrentStock, MaxStock)
        VALUES (?, ?, ?)
    ''', (item_id, current_stock, max_stock))
    conn.commit()
    conn.close()

def get_items():
    conn = sqlite3.connect('database.db')
    cursor = conn.execute('''
        SELECT ItemID, CurrentStock, MaxStock, MinStock
        FROM Stock
    ''')
    result = cursor.fetchall()
    conn.close()
    return result # Returns list of tuples

def get_price(item_id, buy_or_sell):
    conn = sqlite3.connect('database.db')
    cursor = conn.execute('''
        SELECT BuyPrice, SellPrice
        FROM Exchange
        WHERE ItemID = ?
    ''', (item_id,))
    result = cursor.fetchone()
    conn.close()
    if buy_or_sell == 0:
        return result[0]
    else:
        return result[1]

def add_exchange(display_name, item_id, change_count, buy_price, sell_price, min_sell_amount):
    conn = sqlite3.connect('database.db')
    conn.execute('''
        INSERT INTO Exchange (DisplayName, ItemID, ChangeCount, BuyPrice, SellPrice, MinSellAmount)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (display_name, item_id, change_count, buy_price, sell_price, min_sell_amount))
    conn.commit()
    conn.close()

def exchange(item_id, change_count):
    conn = sqlite3.connect('database.db')
    conn.execute('''
        UPDATE Stock
        SET CurrentStock = CurrentStock + ?
        WHERE ItemID = ?
    ''', (change_count, item_id))
    conn.commit()
    conn.close()

#Area codes: 0 For purchase, 1,2,3 for sale
def add_stats(item_id, operation, amount, area):
    conn = sqlite3.connect('database.db')
    conn.execute('''
        INSERT INTO Stats (ItemID, Operation, Amount, Area)
        VALUES (?, ?, ?, ?)
    ''', (item_id, operation, amount, area))
    conn.commit()
    conn.close()

def add_discount(item_id, buy_discount, sell_discount):
    conn = sqlite3.connect('database.db')
    conn.execute('''
        INSERT INTO Discount (ItemID, BuyDiscount, SellDiscount)
        VALUES (?, ?, ?)
    ''', (item_id, buy_discount, sell_discount))
    conn.commit()
    conn.close()

def get_discount(item_id, buy_or_sell):
    conn = sqlite3.connect('database.db')
    cursor = conn.execute('''
        SELECT BuyDiscount, SellDiscount
        FROM Discount
        WHERE ItemID = ?
    ''', (item_id,))
    result = cursor.fetchone()
    conn.close()
    if buy_or_sell == 0:
        return result[0]
    else:
        return result[1]



def set_defaults():
    #Add users
    add_user('001', 'Stanley Hudson', 'Buyer')
    add_user('002', 'Angela Martin', 'Buyer')
    add_user('003', 'Dwight Schrute', 'Seller')
    add_user('004', 'Jim Halpert', 'Seller')
    add_user('005', 'Andy Bernard', 'Seller')

    #Add stock items
    add_item('A2', 0, 100)
    add_item('A3', 0, 150)
    add_item('A4', 0, 400)
    add_item('A5', 0, 150)
    add_item('A6', 0, 300)

    add_item('C2', 0, 100)
    add_item('C3', 0, 300)
    add_item('C4', 0, 400)
    add_item('C5', 0, 150)
    add_item('C6', 0, 300)

    add_item('A3P', 0, 1)
    add_item('A4P', 0, 1)

    #Add exchange items
    add_exchange('Paper A2', 'A2', 1, 18.95, 24.15, 20)
    add_exchange('Paper A3', 'A3', 1, 11.34, 13.25, 30)
    add_exchange('Paquet x5 A3', 'A3', 5, 58.45, 63.95, 1)
    add_exchange('Paper A4', 'A4', 1, 7.98, 9.45, 100)
    add_exchange('Paquet x5 A4', 'A4', 5, 37.65, 42.95, 1)
    add_exchange('Paper A5', 'A5', 1, 7.13, 8.10, 50)
    add_exchange('Paper A6', 'A6', 1, 6.45, 7.45, 60)

    add_exchange('Paper C2', 'C2', 1, 33.45, 35.45, 20)
    add_exchange('Paper C3', 'C3', 1, 30.58, 32.68, 30)
    add_exchange('Paper C4', 'C4', 1, 24.78, 26.74, 60)
    add_exchange('Paper C5', 'C5', 1, 20.80, 22.95, 40)
    add_exchange('Paper C6', 'C6', 1, 16.15, 17.15, 100)

    #Add discounts
    add_discount('A2', 0.07, 0.05)
    add_discount('A3', 0.06, 0.04)
    add_discount('A4', 0.05, 0.03)
    add_discount('A5', 0.04, 0.02)
    add_discount('A6', 0.03, 0.01)

    add_discount('C2', 0.07, 0.05)
    add_discount('C3', 0.06, 0.04)
    add_discount('C4', 0.05, 0.03)
    add_discount('C5', 0.04, 0.02)
    add_discount('C6', 0.03, 0.01)

    add_discount('A3P', 0.03, 0.02)
    add_discount('A4P', 0.02, 0.015)



if __name__ == '__main__':
    create_db()
    set_defaults()