<<<<<<< HEAD
from flask import Flask, jsonify, render_template, request
=======
from flask import Flask, jsonify, request, render_template
>>>>>>> 8b75e7e037f5c3e35cfaa81d7496c3e7dad0e62a
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import os

# Initialize Flask app
app = Flask(__name__, template_folder='templates')

# Configuration
app.config['MONGODB_SETTINGS'] = {
    'db': 'game_db',
    'host': 'localhost',
    'port': 27017
}
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "default_secret_key")  # Use environment variable
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize extensions
db = MongoEngine(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Models
class User(db.Document):
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)

class Score(db.Document):
    user_id = db.ReferenceField(User, required=True)
    score = db.IntField(required=True)
    created_at = db.DateTimeField(auto_now_add=True)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if User.objects(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, password=hashed_password)
    user.save()

    return jsonify({"message": "User created successfully"}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.objects(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"token": access_token}), 200

@app.route('/api/game/submit', methods=['POST'])
@jwt_required()
def submit_score():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    score_value = data.get('score')

    if not score_value or not isinstance(score_value, int):
        return jsonify({"error": "Valid score is required"}), 400

    score = Score(user_id=current_user_id, score=score_value)
    score.save()

    return jsonify({"message": "Score submitted successfully"}), 201

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    top_scores = Score.objects.order_by('-score').limit(10)
    leaderboard = []

    for score in top_scores:
        user = User.objects(id=score.user_id.id).first()
        leaderboard.append({
            "username": user.username,
            "score": score.score,
            "created_at": score.created_at
        })

    return jsonify(leaderboard), 200

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Route not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "An internal error occurred"}), 500

# Main entry point
if __name__ == '__main__':
    app.run(debug=True) 