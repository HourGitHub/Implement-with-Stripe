from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.before_request
def before_request():
    if 'cart' not in session:
        session['cart'] = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    response = requests.get(f'https://dummyjson.com/products/{product_id}')
    product = response.json()
    if product:
        cart = session['cart']
        for item in cart:
            if item['id'] == product_id:
                item['quantity'] += 1
                session['cart'] = cart
                return redirect(url_for('cart_page'))
        product['quantity'] = 1
        cart.append(product)
        session['cart'] = cart
    return redirect(url_for('cart_page'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session['cart']
    for item in cart:
        if item['id'] == product_id:
            if item['quantity'] > 1:
                item['quantity'] -= 1
            else:
                cart.remove(item)
            session['cart'] = cart
            break
    return redirect(url_for('cart_page'))

@app.route('/cart')
def cart_page():
    return render_template('cart.html', cart=session['cart'])

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        card_info = request.form['card_info']
        session['cart'] = []
        return render_template('order_success.html', name=name)
    return render_template('order.html', cart=session['cart'])

if __name__ == '__main__':
    app.run(debug=True)
