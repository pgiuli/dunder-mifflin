import sqlite3

def create_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS Capital (
            Amount REAL NOT NULL
        )
    ''')
    conn.execute('''
         INSERT INTO Capital (Amount) VALUES (0)
        ''')


    conn.execute('''
        CREATE TABLE IF NOT EXISTS Stock (
            ItemID TEXT NOT NULL,
            CurrentStock INTEGER NOT NULL,
            MaxStock INTEGER NOT NULL,
            DisplayName TEXT NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS Exchange (
            DisplayName TEXT NOT NULL,
            ExchangeID TEXT NOT NULL,
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
            ExchangeID TEXT NOT NULL,
            BuyDiscount REAL NOT NULL,
            SellDiscount REAL NOT NULL,
            FOREIGN KEY(ExchangeID) REFERENCES Exchange(ExchangeID)
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS Stats (
            ExchangeID TEXT NOT NULL,
            Operation TEXT NOT NULL,
            Amount INTEGER NOT NULL,
            Area INTEGER NOT NULL,
            ClientID TEXT NOT NULL,
            UserID TEXT NOT NULL,
            FOREIGN KEY(ExchangeID) REFERENCES Exchange(ItemID)
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            UserID TEXT PRIMARY KEY,
            Password TEXT NOT NULL,
            DisplayName TEXT NOT NULL,
            Role TEXT NOT NULL
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS Clients (
            ClientID TEXT PRIMARY KEY,
            DisplayName TEXT NOT NULL,
            Area INTEGER NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def add_user(user_id, password, display_name, role):
    conn = sqlite3.connect('database.db')
    conn.execute('''
        INSERT INTO Users (UserID, Password, DisplayName, Role)
        VALUES (?, ?, ?, ?)
    ''', (user_id, password, display_name, role))
    conn.commit()
    conn.close()

def get_user(user_id): # Returns tuple
    conn = sqlite3.connect('database.db')
    cursor = conn.execute('''
        SELECT UserID, Password, DisplayName, Role
        FROM Users
        WHERE UserID = ?
    ''', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def get_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.execute('''
        SELECT UserID, Password, DisplayName, Role
        FROM Users
    ''')
    result = cursor.fetchall()
    conn.close()
    return result

def add_item(item_id, current_stock, max_stock, display_name):
    conn = sqlite3.connect('database.db')
    conn.execute('''
        INSERT INTO Stock (ItemID, CurrentStock, MaxStock, DisplayName)
        VALUES (?, ?, ?, ?)
    ''', (item_id, current_stock, max_stock, display_name))
    conn.commit()
    conn.close()

def get_stock(): # Returns dict of tuples
    conn = sqlite3.connect('database.db')
    cursor = conn.execute('''
        SELECT ItemID, CurrentStock, MaxStock, DisplayName
        FROM Stock
    ''')
    result = cursor.fetchall()
    conn.close()
    stock = {}
    for item in result:
        stock[item[0]] = item
    return stock

def get_price(exchange_id, buy_or_sell):
    conn = sqlite3.connect('database.db')
    cursor = conn.execute('''
        SELECT BuyPrice, SellPrice
        FROM Exchange
        WHERE ExchangeID = ?
    ''', (exchange_id,))
    result = cursor.fetchone()
    conn.close()
    if buy_or_sell == 0:
        return result[0]
    else:
        return result[1]

def add_exchange(display_name, exchange_id, item_id, change_count, buy_price, sell_price, min_sell_amount):
    conn = sqlite3.connect('database.db')
    conn.execute('''
        INSERT INTO Exchange (DisplayName, ExchangeID, ItemID, ChangeCount, BuyPrice, SellPrice, MinSellAmount)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (display_name, exchange_id, item_id, change_count, buy_price, sell_price, min_sell_amount))
    conn.commit()
    conn.close()

def get_exchanges():
    conn = sqlite3.connect('database.db')
    cursor = conn.execute('''
        SELECT DisplayName, ExchangeID, ItemID, ChangeCount, BuyPrice, SellPrice, MinSellAmount
        FROM Exchange
    ''')
    result = cursor.fetchall()
    conn.close()
    return result # Returns list of tuples

def update_stock(item_id, change_count):
    conn = sqlite3.connect('database.db')
    conn.execute('''
        UPDATE Stock
        SET CurrentStock = CurrentStock + ?
        WHERE ItemID = ?
    ''', (change_count, item_id))
    conn.commit()
    conn.close()

#Area codes: 0 For purchase, 1,2,3 for sale
def add_stats(exchange_id, operation, amount, area, client_id, user_id):
    conn = sqlite3.connect('database.db')
    conn.execute('''
        INSERT INTO Stats (ExchangeID, Operation, Amount, Area, ClientID, UserID)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (exchange_id, operation, amount, area, client_id, user_id))
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect('database.db')
    cursor = conn.execute('''
        SELECT ExchangeID, Operation, Amount, Area, ClientID, UserID
        FROM Stats
    ''')
    result = cursor.fetchall()
    conn.close()
    return result

def add_discount(exchange_id, buy_discount, sell_discount):
    conn = sqlite3.connect('database.db')
    conn.execute('''
        INSERT INTO Discount (ExchangeID, BuyDiscount, SellDiscount)
        VALUES (?, ?, ?)
    ''', (exchange_id, buy_discount, sell_discount))
    conn.commit()
    conn.close()

def get_discount(exchange_id, buy_or_sell):
    conn = sqlite3.connect('database.db')
    cursor = conn.execute('''
        SELECT BuyDiscount, SellDiscount
        FROM Discount
        WHERE ExchangeID = ?
    ''', (exchange_id,))
    result = cursor.fetchone()
    conn.close()
    if buy_or_sell == 0:
        return result[0]
    else:
        return result[1]

def change_capital(amount):
    amount = round(amount,2)
    conn = sqlite3.connect('database.db')
    conn.execute('''
        UPDATE Capital
        SET Amount = Amount + ?
    ''', (amount,))
    conn.commit()
    conn.close()

def get_capital():
    conn = sqlite3.connect('database.db')
    cursor = conn.execute('''
        SELECT Amount
        FROM Capital
    ''')
    result = cursor.fetchone()
    conn.close()
    return round(result[0],2)

def add_client(client_id, display_name, area):
    conn = sqlite3.connect('database.db')
    conn.execute('''
        INSERT INTO Clients (ClientID, DisplayName, Area)
        VALUES (?, ?, ?)
    ''', (client_id, display_name, int(area)))
    conn.commit()
    conn.close()

def get_clients():
    conn = sqlite3.connect('database.db')
    cursor = conn.execute('''
        SELECT ClientID, DisplayName, Area
        FROM Clients
    ''')
    result = cursor.fetchall()
    conn.close()
    return result


def set_defaults():
    #Add users
    add_user('stanley', '001', 'Stanley Hudson', 'Buyer')
    add_user('angela', '002', 'Angela Martin', 'Buyer')
    add_user('dwight', '003', 'Dwight Schrute', 'Seller')
    add_user('jim', '004', 'Jim Halpert', 'Seller')
    add_user('andy', '005', 'Andy Bernard', 'Seller')

    #Add stock items
    add_item('A2', 0, 100, 'Paper A2')
    add_item('A3', 0, 150, 'Paper A3')
    add_item('A4', 0, 400, 'Paper A4')
    add_item('A5', 0, 150, 'Paper A5')
    add_item('A6', 0, 300, 'Paper A6')

    add_item('C2', 0, 100, 'Sobre C2')
    add_item('C3', 0, 300, 'Sobre C3')
    add_item('C4', 0, 400, 'Sobre C4')
    add_item('C5', 0, 150, 'Sobre C5')
    add_item('C6', 0, 300, 'Sobre C6')

    #Add exchange items
    add_exchange('Paper A2', 'A2', 'A2', 1, 18.95, 24.15, 20)
    add_exchange('Paper A3', 'A3', 'A3', 1, 11.34, 13.25, 30)
    add_exchange('Paquet x5 A3', 'A3P', 'A3', 5, 58.45, 63.95, 1)
    add_exchange('Paper A4', 'A4', 'A4', 1, 7.98, 9.45, 100)
    add_exchange('Paquet x5 A4', 'A4P', 'A4', 5, 37.65, 42.95, 1)
    add_exchange('Paper A5', 'A5', 'A5', 1, 7.13, 8.10, 50)
    add_exchange('Paper A6', 'A6', 'A6', 1, 6.45, 7.45, 60)

    add_exchange('Sobre C2', 'C2', 'C2', 1, 33.45, 35.45, 20)
    add_exchange('Sobre C3', 'C3', 'C3', 1, 30.58, 32.68, 30)
    add_exchange('Sobre C4', 'C4', 'C4', 1, 24.78, 26.74, 60)
    add_exchange('Sobre C5', 'C5', 'C5', 1, 20.80, 22.95, 40)
    add_exchange('Sobre C6', 'C6', 'C6', 1, 16.15, 17.15, 100)

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

    #Add clients
    add_client('mitch', 'Mitch Smith ', 1)
    add_client('pam', 'Pam Rogers', 1)
    add_client('michael', 'Michael Reeves', 2)
    add_client('kevin', 'Kevin Malone', 2)
    add_client('oscar', 'Oscar Martinez', 3)
    add_client('toby', 'Toby Flenderson', 3)
    add_client('phyllis', 'Phyllis Vance', 3)


    change_capital(10000)
    


if __name__ == '__main__':
    create_db()
    set_defaults()