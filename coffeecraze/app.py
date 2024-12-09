from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import os

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coffeecraze.db'  # Path to your SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "default_secret_key")
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "default_secret_key")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class CoffeeShop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    logo_url = db.Column(db.String(250))
    description = db.Column(db.String(250))

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    coffee_shop_id = db.Column(db.Integer, db.ForeignKey('coffee_shop.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    coffee_shop_id = db.Column(db.Integer, db.ForeignKey('coffee_shop.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return jsonify({"error": "Passwords do not match"}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return jsonify({"error": "User already exists"}), 400
        
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/game', methods=['GET', 'POST'])
def game():
    coffee_shops = CoffeeShop.query.all()
    
    # Debugging
    print("Coffee Shops:", coffee_shops)

    # If there are no coffee shops in the database, handle the case
    if not coffee_shops:
        return render_template('game.html', coffee_shops=[])

    if request.method == 'POST':
        pass

    return render_template('game.html', coffee_shops=coffee_shops)


@app.route('/leaderboard')
def leaderboard():
    leaderboard_data = (
        db.session.query(
            CoffeeShop.name,
            db.func.count(Score.id).label('votes')
        )
        .join(Score, CoffeeShop.id == Score.coffee_shop_id)
        .group_by(CoffeeShop.id)
        .order_by(db.func.count(Score.id).desc())
        .all()
    )
    return render_template('leaderboard.html', leaderboard=leaderboard_data)

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        user_id = session.get('user_id')
        coffee_shop_id = request.form.get('coffee_shop_id')
        content = request.form.get('content')

        if not user_id or not coffee_shop_id or not content:
            return jsonify({"error": "All fields are required"}), 400

        new_review = Review(user_id=user_id, coffee_shop_id=coffee_shop_id, content=content)
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for('reviews'))

    coffee_shops = CoffeeShop.query.all()
    reviews = (
        db.session.query(Review, CoffeeShop.name)
        .join(CoffeeShop, Review.coffee_shop_id == CoffeeShop.id)
        .all()
    )
    return render_template('reviews.html', coffee_shops=coffee_shops, reviews=reviews)

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Route not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "An internal error occurred"}), 500

# Main entry point
if __name__ == '__main__':
<<<<<<< HEAD
    db.create_all()  # Ensure database tables exist
    app.run(debug=True)


=======
    with app.app_context():
        db.create_all()  # Ensure database tables exist
    app.run(debug=True, port=5001)
>>>>>>> f8bd1f34bcf91b8df1075e0519f18b7c67a6e24d
