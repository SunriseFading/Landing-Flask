from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, Checkout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(15), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    description = db.Column(db.String(50))

    def __repr__(self):
        return f'Position: {self.id} {self.title} {self.price} {self.description}'


@app.route('/')
def index():
    positions = Position.query.order_by(Position.price).all()
    return render_template('index.html', data=positions)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/buy/<int:id>')
def buy(id):
    position = Position.query.get(id)
    api = Api(merchant_id=1396424,secret_key='test')
    checkout = Checkout(api=api)
    data = {
    "currency": "USD",
    "amount": str(position.price) + '00'
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method != 'POST':
        return render_template('create.html')
    title = request.form['title']
    price = request.form['price']
    description = request.form['description']
    position = Position(title=title, price=price, description=description)
    try:
        db.session.add(position)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error'


if __name__ == '__main__':
    app.run(debug=True)
