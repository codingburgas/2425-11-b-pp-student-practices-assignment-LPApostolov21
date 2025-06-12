from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import logout_user
from werkzeug.security import generate_password_hash
from forms import RegisterForm, LoginForm
from models import db, User, Admin
from werkzeug.security import check_password_hash


auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        role = form.role.data
        hashed_password = generate_password_hash(password, method='scrypt')

        if role == 'admin':
            existing_admin = Admin.query.filter_by(username_admin=username).first()
            if existing_admin:
                flash('This admin already exists. Please choose a different username.', 'warning')
                return render_template('register.html', form=form)
            new_admin = Admin(username_admin=username, password_hash=hashed_password, role=role)
            db.session.add(new_admin)
            flash('Admin account created successfully!', 'success')
        else:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('This user already exists. Please choose a different username.', 'warning')
                return render_template('register.html', form=form)
            new_user = User(username=username, password_hash=hashed_password, role=role)
            db.session.add(new_user)
            flash('User account created successfully!', 'success')

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
        existing_user_admin = Admin.query.filter_by(username_admin=username).first()
        if existing_user_admin == username and check_password_hash(existing_user.password_hash, password):
            flash('Login successful!', "success")
            return redirect(url_for('main.admin_main'))


        if existing_user_admin and check_password_hash(existing_user_admin.password_hash, password):
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