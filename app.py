from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from Mech.auth import auth as auth_blueprint
from Mech.main import main as main_blueprint
from models import db, User, Admin

# Initialize Mail outside create_app for import elsewhere
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'my_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Flask-Mail config
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'LPApostolov21@codingburgas.bg'
    app.config['MAIL_PASSWORD'] = 'my_secret_key'
    app.config['MAIL_DEFAULT_SENDER'] = 'ktotev@codingburgas.bg'

    # Initialize extensions with app
    db.init_app(app)
    mail.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id)) or Admin.query.get(int(user_id))

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
