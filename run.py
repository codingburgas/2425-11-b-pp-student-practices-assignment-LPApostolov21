from flask import Flask
from Mech.auth import auth as auth_blueprint
from Mech.main import main as main_blueprint
from models import db, User
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'my_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    db.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    if not os.path.exists('site.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)