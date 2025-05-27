from flask import Blueprint, render_template, redirect, url_for
from werkzeug.security import generate_password_hash

from forms import RegisterForm
from models import db, User



auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('register.html', form=form)
        hashed_password = generate_password_hash(password, method='scrypt')
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@auth.route('/login')
def login():
    return "Login Page"

@auth.route('/logout')
def logout():
    return "Logout Page"
