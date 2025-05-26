from flask import Blueprint

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def index():
    return "Welcome to the Main Page"

@main.route('/about')
def about():
    return "About Page"
