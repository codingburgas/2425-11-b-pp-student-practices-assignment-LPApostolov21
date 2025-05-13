from flask import Flask
from Mech.auth import auth as auth_blueprint
from Mech.main import main as main_blueprint

def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)