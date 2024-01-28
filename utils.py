import db

def calc_price(exchange_id, amount, buy_or_sell):
    price = 0
    unit_price = db.get_price(exchange_id, buy_or_sell)

    if amount >= 4: #Elegible for discount.
        discount_percentage = db.get_discount(exchange_id, buy_or_sell)
        price += ((amount // 4) * 4) * unit_price * (1 - discount_percentage)
    
    price += (amount % 4) * unit_price

    return round(price,2)






#Test

print(calc_price("A4",1,0)) #Buy
print(calc_price("A4",1,1)) #Sell

print(calc_price("A4",4,0)) #Buy
print(calc_price("A4",4,1)) #Sell

print(calc_price("A4P",1,0)) #Buy
print(calc_price("A4P",1,1)) #Sell
