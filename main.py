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
    return render_template('index.html')

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
    if current_user.role == 'Buyer':
        return render_template('buyer_dashboard.html', user=current_user, stock=db.get_stock(), capital=db.get_capital())
    elif current_user.role == 'Seller':
        return render_template('seller_dashboard.html')

@website.route('/purchase', methods=['POST', 'GET'])
@login_required
def purchase():
    if current_user.role != 'Buyer':
        return redirect('/dashboard')
    if request.method == 'POST':
        status = utils.purchase(request.form)
        return render_template('purchase_after.html', status=status)
    elif request.method == 'GET':
        db_exchanges = db.get_exchanges()
        #print(db_exchanges)
        exchanges = []
        for exchange in db_exchanges:
            exchanges.append({
                'display_name': exchange[0],
                'exchange_id': exchange[1],
                'buy_price': exchange[4]
            })
        return render_template('purchase.html', exchanges=exchanges)

@website.route('/sell', methods=['POST', 'GET'])
@login_required
def sell():
    if current_user.role != 'Seller':
        return redirect('/dashboard')
    if request.method == 'POST':
        print(request.form)
        status = utils.sell(request.form)
        return render_template('sell_after.html', status=status)
    elif request.method == 'GET':
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
        return render_template('sell.html', exchanges=exchanges)

@website.route('/logout')
def logout():
    logout_user()
    return redirect('/')

if __name__ == '__main__':
    website.run(debug=True)