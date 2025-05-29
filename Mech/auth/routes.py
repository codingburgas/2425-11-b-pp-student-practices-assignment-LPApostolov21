from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import logout_user
from werkzeug.security import generate_password_hash
from forms import RegisterForm, LoginForm
from models import db, User
from werkzeug.security import check_password_hash


auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('This user already exists. Please choose a different email or username.', 'warning')
            return render_template('register.html', form=form)
        hashed_password = generate_password_hash(password, method='scrypt')
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        existing_user = User.query.filter_by(username=username).first()

        if existing_user and check_password_hash(existing_user.password_hash, password):
            flash("Login successful!", "success")
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))