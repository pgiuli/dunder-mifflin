import db

options = {
    '1' : 'Inicialitzar la base de dades',
    '2' : 'Afegir un nou client',
    '3' : 'Afegir un nou producte',
    '4' : 'Afegir un nou usuari',
    '5' : 'Afegir un nou intercanvi',
    '6' : 'Afegir un nou descompte',
    '7' : 'Modificar capital',
    '8' : 'Soritir'
}


def print_options():
    for key in options:
        print(f'{key}. {options[key]}')

while True:
    print_options()
    option = input('Escull una opció: ')
    match option:
        case '1':
            db.create_db()
        case '2':
            username = input("Nom d'usuari: ")
            name = input("Nom: ")
            area = input("Àrea: ")
            db.add_client(username, name, area)
        case '3':
            item_id = input("ID del producte: ")
            stock = input("Stock: ")
            max_stock = input("Stock màxim: ")
            name = input("Nom del producte: ")
            db.add_item(item_id, stock, max_stock, name)
        case '4':
            username = input("Nom d'usuari: ")
            password = input("Contrasenya: ")
            display_name = input("Nom: ")
            role = input("Rol: ")
            db.add_user(username, password, display_name, role)
        case '5':
            display_name = input("Nom: ")
            exchange_id = input("ID de l'intercanvi: ")
            item_id = input("ID del producte (a stock): ")
            amount = input("Quantitat a intercanviar (Paquets): ")
            buy_price = input("Preu de compra: ")
            sell_price = input("Preu de venda: ")
            min_sell_amount = input("Quantitat mínima de venda: ")
            db.add_exchange(display_name, buy_price, sell_price, min_sell_amount)
        case '6':
            exchange_id = input("ID de l'intercanvi: ")
            buy_discount = input("Descompte de compra (decimal): ")
            sell_discount = input("Descompte de venda: (decimal): ")
            db.add_discount(exchange_id, buy_discount, sell_discount)
        case '7':
            capital = input("Capital (positiu per a afegir, negatiu per a retirar): ")
            db.change_capital(capital)