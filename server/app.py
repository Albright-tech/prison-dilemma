from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, set_access_cookies, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from models import  db, User, UserRole, GameScore

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'M1U5T6VDFH68'  # Change this to a strong, random key
app.config['JWT_SECRET_KEY'] = 'FG89JK07GVC5'  # Change this to a strong, random key
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
db.init_app(app)


migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


decisions = {}
@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.json

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'Incomplete data'}), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'message': 'Username or email already exists'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.id)
    resp = jsonify({'message': 'User registered successfully!', 'token': access_token})
    set_access_cookies(resp, access_token)
    return resp, 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Incomplete data'}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        resp = jsonify({'message': 'Invalid credentials'})
        unset_jwt_cookies(resp)
        return resp, 401

    access_token = create_access_token(identity=user.id)
    resp = jsonify({'login': True, 'token': access_token})
    set_access_cookies(resp, access_token)
    return resp, 200

@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify(logged_in_as=current_user_id), 200

@app.route('/api/user/<string:username>', methods=['PATCH'])
@jwt_required()
def update_user(username):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user or not bcrypt.check_password_hash(current_user.password, request.json.get('current_password')):
        return jsonify({'message': 'Invalid credentials'}), 401

    user_to_update = User.query.filter_by(username=username).first()

    if not user_to_update:
        return jsonify({'message': 'User not found'}), 404

    data = request.json

    # Update only the fields that are present in the request
    if 'new_username' in data:
        user_to_update.username = data['new_username']
    if 'new_email' in data:
        user_to_update.email = data['new_email']
    if 'new_password' in data:
        user_to_update.password = bcrypt.generate_password_hash(data['new_password']).decode('utf-8')

    db.session.commit()

    return jsonify({'message': 'User updated successfully'}), 200

@app.route('/api/user/<string:username>', methods=['DELETE'])
@jwt_required()
def delete_user(username):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user or not bcrypt.check_password_hash(current_user.password, request.json.get('password')):
        return jsonify({'message': 'Invalid credentials'}), 401

    user_to_delete = User.query.filter_by(username=username).first()

    if not user_to_delete:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user_to_delete)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'}), 200

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200

@app.route('/api/scores/<int:score_id>', methods=['DELETE'])
@jwt_required()
def delete_score(score_id):
    try:
        score_to_delete = GameScore.query.get(score_id)
        if not score_to_delete:
            return jsonify({'message': 'Score not found'}), 404

        db.session.delete(score_to_delete)
        db.session.commit()

        return jsonify({'message': 'Score deleted successfully'}), 200

    except Exception as e:
        return jsonify({'message': f'Error deleting score: {str(e)}'}), 500
    

if __name__ == '__main__':
 app.run(port=5000, debug=True)
