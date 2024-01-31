from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    scores = db.relationship('GameScore', backref='user', lazy=True)

class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False)
    users = db.relationship('User', secondary='user_roles', backref='roles', lazy=True)

user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('user_role.id'), primary_key=True)
)

class GameScore(db.Model):
    __tablename__ = 'game_score'
    id = db.Column(db.Integer, primary_key=True)
    total_jail_years_player1 = db.Column(db.Integer, nullable=False)
    total_jail_years_player2 = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class UserRoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserRole

class GameScoreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GameScore

# Initialize marshmallow for serialization
user_schema = UserSchema()
user_role_schema = UserRoleSchema()
game_score_schema = GameScoreSchema()
