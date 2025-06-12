from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='user')

    def password(self, plaintext_password):
        self.password_hash = generate_password_hash(plaintext_password)

    def verify_password(self, plaintext_password):
        return check_password_hash(self.password_hash, plaintext_password)

class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_brand = db.Column(db.String(20), nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    man_year = db.Column(db.Integer, nullable=False)

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username_admin = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='user')

    def password_admin(self, plaintext_password):
        self.password_hash = generate_password_hash(plaintext_password)

    def verify_password_admin(self, plaintext_password):
        return check_password_hash(self.password_hash, plaintext_password)