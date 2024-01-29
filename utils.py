import db

def calc_price(exchange_id, amount, buy_or_sell):
    amount = int(amount)
    price = 0
    unit_price = db.get_price(exchange_id, buy_or_sell)

    if amount >= 4: #Elegible for discount.
        discount_percentage = db.get_discount(exchange_id, buy_or_sell)
        price += ((amount // 4) * 4) * unit_price * (1 - discount_percentage)
    
    price += (amount % 4) * unit_price

    return round(price,2)


def purchase(request_dict):
    request_dict = request_dict.to_dict()
    errors = []

    total_cost = 0
    available_capital = db.get_capital()
    db_stock = db.get_stock()
    #print(db_stock)

    #Check if max_stock is exceeded
    stock_dict = {}
    for item in request_dict:
        #print(item)
        #print(request_dict[item])
        if request_dict[item] == '':
            if 'P' not in item:
                stock_dict[item] = 0
        elif 'P' in item:
            #print(purchase_dict[item[:-1]])
            stock_dict[item[:-1]] += int(request_dict[item]) * 5
        else:
            stock_dict[item] = int(request_dict[item])
    
    #print(purchase_dict)
    for item in stock_dict:
        available_stock = db_stock[item][2] - db_stock[item][1]
        if stock_dict[item] > available_stock:
            errors.append(f'Not enough space for {item}. Available space: {available_stock}')
    
    #Check if capital is exceeded
    for item in request_dict:
        if request_dict[item] == '':
            continue
        total_cost += calc_price(item, request_dict[item], 0)

    #Calc IVA
    total_cost = round(total_cost*1.21,2)
    if total_cost > available_capital:
        errors.append(f'Not enough capital. Available capital: {available_capital}')
    
    print(total_cost)
    if len(errors) > 0:
        return errors
    else:
        for item in stock_dict:
            quantity = stock_dict[item]
            if quantity == 0:
                continue
            db.update_stock(item, quantity)
            #db.add_stats(item, 0, quantity, 0)
        db.change_capital(-total_cost)
        return 'Purchase successful!!!'

def sell(request_dict):
    request_dict = request_dict.to_dict()
    #Remove 'Sell Area' from request_dict
    area = request_dict.pop('Sell Area')
    errors = []
    print(request_dict)
    total_profit = 0
    db_stock = db.get_stock()
    #print(db_stock)

    #Check if max_stock is exceeded
    stock_dict = {}
    for item in request_dict:
        #print(item)
        #print(request_dict[item])
        if request_dict[item] == '':
            if 'P' not in item:
                stock_dict[item] = 0
        elif 'P' in item:
            #print(purchase_dict[item[:-1]])
            stock_dict[item[:-1]] += int(request_dict[item]) * 5
        else:
            stock_dict[item] = int(request_dict[item])
    
    #print(purchase_dict)
    for item in stock_dict:
        available_stock = db_stock[item][1]
        if stock_dict[item] > available_stock:
            errors.append(f'Not enough stock for {item}. Available stock: {available_stock}')
    
    #Calc final sell price
    for item in request_dict:
        if request_dict[item] == '':
            continue
        total_profit += calc_price(item, request_dict[item], 1)

    #Calc shipping cost
    if total_profit <= 499:
        total_profit += 19.95
    elif total_profit <= 999:
        total_profit += 9.95


    #Calc IVA
    total_profit = round(total_profit*1.21,2)
    
    print(total_profit)
    if len(errors) > 0:
        return errors
    else:
        for item in stock_dict:
            quantity = stock_dict[item]
            if quantity == 0:
                continue
            db.update_stock(item, -quantity)
            db.add_stats(item, 1, quantity, area)
        db.change_capital(total_profit)
        return 'Sale successful!!!'


    




#Test

#print(calc_price("A4",1,0)) #Buy
#print(calc_price("A4",1,1)) #Sell

#print(calc_price("A4",4,0)) #Buy
#print(calc_price("A4",4,1)) #Sell

#print(calc_price("A4P",1,0)) #Buy
#print(calc_price("A4P",1,1)) #Sell
