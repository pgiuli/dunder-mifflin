from flask import Flask, request, redirect, render_template, session
from flask_login import current_user, UserMixin, LoginManager, login_required, login_user, logout_user
import db
import utils

website = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(website)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    user_info = db.get_user(user_id)
    if user_info:
        return User(*user_info)
    return None

website.secret_key = 'secret'
class User(UserMixin):
    def __init__(self, user_id, password, display_name, role):
        self.id = user_id
        self.password = password
        self.display_name = display_name
        self.role = role
    
    @property
    def is_authenticated(self):
        return True
    
    def get_id(self):
        return str(self.id)

@website.route('/')
def index():
    #If logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect('/dashboard')
    else:
        return redirect('/login')

@website.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        user_info = db.get_user(user_id)
        if user_info:
            user = User(*user_info)
            if user.password == password:
                login_user(user)
                return redirect('/dashboard')
    return render_template('login.html')


@website.route('/dashboard')
@login_required
def dashboard():
    print(current_user.id)
    return render_template('dashboard.html', user=current_user, stock=db.get_stock(), capital=db.get_capital())

@website.route('/purchase', methods=['POST', 'GET'])
@login_required
def purchase():
    if current_user.role != 'Buyer':
        return redirect('/dashboard')
    if request.method == 'POST':
        db_exchanges = db.get_exchanges()
        exchanges = []
        for exchange in db_exchanges:
            exchanges.append({
                'display_name': exchange[0],
                'exchange_id': exchange[1],
                'buy_price': exchange[4]
            })
        status = utils.purchase(request.form, user_id=current_user.id)
        #shutup
        if type(status) != list:
            status = [status]
        return render_template('purchase.html', exchanges=exchanges, status=status, user=current_user)
    elif request.method == 'GET':
        db_exchanges = db.get_exchanges()
        exchanges = []
        for exchange in db_exchanges:
            exchanges.append({
                'display_name': exchange[0],
                'exchange_id': exchange[1],
                'buy_price': exchange[4]
            })
        return render_template('purchase.html', exchanges=exchanges, user=current_user)

@website.route('/sell', methods=['POST', 'GET'])
@login_required
def sell():
    if current_user.role != 'Seller':
        return redirect('/dashboard')
    if request.method == 'POST':
        clients = db.get_clients()
        db_exchanges = db.get_exchanges()
        #print(db_exchanges)
        exchanges = []
        for exchange in db_exchanges:
            exchanges.append({
                'display_name': exchange[0],
                'exchange_id': exchange[1],
                'sell_price': exchange[5],
                'min_sell_amount': exchange[6]
            })
        status = utils.sell(request.form, user_id=current_user.id)
        #shutup
        if type(status) != list:
            status = [status]
        return render_template('sell.html',exchanges=exchanges, status=status, clients=clients, user=current_user)
    elif request.method == 'GET':
        clients = db.get_clients()
        print(clients)
        db_exchanges = db.get_exchanges()
        #print(db_exchanges)
        exchanges = []
        for exchange in db_exchanges:
            exchanges.append({
                'display_name': exchange[0],
                'exchange_id': exchange[1],
                'sell_price': exchange[5],
                'min_sell_amount': exchange[6]
            })
        return render_template('sell.html', exchanges=exchanges, clients=clients, user=current_user)

@website.route('/stats', methods=['GET'])
@login_required
def stats():
    stats = db.get_stats()
    #print(stats)
    clients = db.get_clients() #For display_name
    #print(clients)
    stock = db.get_stock() #For display_name
    #print(stock)
    return render_template('stats.html', stats=stats, clients=clients, stock=stock, user=current_user)

@website.route('/favicon.ico')
def favicon():
    return website.send_static_file('favicon.ico')

@website.route('/logout')
def logout():
    logout_user()
    return redirect('/')

if __name__ == '__main__':
    website.run(debug=True, host='0.0.0.0', port=5001)