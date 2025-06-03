from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def password(self, plaintext_password):
        self.password_hash = generate_password_hash(plaintext_password)

    def verify_password(self, plaintext_password):
        return check_password_hash(self.password_hash, plaintext_password)

class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_brand = db.Column(db.String(20), nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    man_year = db.Column(db.Integer, nullable=False)