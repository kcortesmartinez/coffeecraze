from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configuration
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "default_secret_key")

# Database helper function
def get_db_connection():
    conn = sqlite3.connect('coffeecraze.db')  # Ensure this file exists
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

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
            return "Passwords do not match!", 400

        # Insert user into the database
        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, password)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            return "User already exists!", 400
        finally:
            conn.close()

        return redirect(url_for('home'))

    return render_template('register.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    conn = get_db_connection()
    coffee_shops = conn.execute("SELECT * FROM coffee_shops").fetchall()
    conn.close()

    if not coffee_shops:
        return render_template('game.html', coffee_shops=[])

    if request.method == 'POST':
        user_id = session.get('user_id')
        coffee_shop_id = request.json.get('coffee_shop_id')

        if not user_id or not coffee_shop_id:
            return "User or Coffee Shop ID missing!", 400

        # Insert vote into rankings table
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO rankings (user_id, coffee_shop_id, rank) VALUES (?, ?, ?)",
            (user_id, coffee_shop_id, 1)  # Replace '1' with the actual rank logic
        )
        conn.commit()
        conn.close()

        return "Vote submitted successfully", 201

    return render_template('game.html', coffee_shops=coffee_shops)

@app.route('/leaderboard')
def leaderboard():
    conn = get_db_connection()
    leaderboard_data = conn.execute("""
        SELECT coffee_shops.name, COUNT(rankings.id) AS votes
        FROM coffee_shops
        LEFT JOIN rankings ON coffee_shops.id = rankings.coffee_shop_id
        GROUP BY coffee_shops.id
        ORDER BY votes DESC
    """).fetchall()
    conn.close()

    return render_template('leaderboard.html', leaderboard=leaderboard_data)

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    conn = get_db_connection()
    coffee_shops = conn.execute("SELECT * FROM coffee_shops").fetchall()
    conn.close()

    if request.method == 'POST':
        user_id = session.get('user_id')
        coffee_shop_id = request.form.get('coffee_shop_id')
        content = request.form.get('content')

        if not user_id or not coffee_shop_id or not content:
            return "All fields are required!", 400

        # Insert review into reviews table
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO reviews (user_id, coffee_shop_id, review, rating) VALUES (?, ?, ?, ?)",
            (user_id, coffee_shop_id, content, 5)  # Replace '5' with actual rating logic
        )
        conn.commit()
        conn.close()

        return redirect(url_for('reviews'))

    conn = get_db_connection()
    reviews = conn.execute("""
        SELECT reviews.review, reviews.rating, coffee_shops.name
        FROM reviews
        JOIN coffee_shops ON reviews.coffee_shop_id = coffee_shops.id
    """).fetchall()
    conn.close()

    return render_template('reviews.html', coffee_shops=coffee_shops, reviews=reviews)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()

        if user and user["password"] == password:
            session['user_id'] = user["id"]
            return redirect(url_for('home'))
        else:
            return "Invalid credentials!", 401

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Main entry point
if __name__ == '__main__':
    app.run(debug=True)




