from flask import Blueprint, render_template

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/main')
def index():
    return render_template('main.html')

@main.route('/about')
def about():
    return "About Page"
