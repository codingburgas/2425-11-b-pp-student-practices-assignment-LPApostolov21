from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm
from models import db, User, Admin

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        role = form.role.data
        hashed_password = generate_password_hash(password, method='scrypt')

        existing_admin = Admin.query.filter_by(username_admin=username).first()
        existing_user = User.query.filter_by(username=username).first()

        if existing_admin or existing_user:
            flash('This username is already taken. Please choose a different one.', 'warning')
            return render_template('register.html', form=form)

        if role == 'admin':
            new_admin = Admin(username_admin=username, password_hash=hashed_password, role=role)
            db.session.add(new_admin)
            db.session.commit()  # <--- FIX: Commit for admin
            flash('Admin account created successfully!', 'success')
            return redirect(url_for('main.admin_main'))
        else:
            new_user = User(username=username, password_hash=hashed_password, role=role)
            db.session.add(new_user)
            db.session.commit()
            flash('User account created successfully!', 'success')
            return redirect(url_for('main.index'))

    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        existing_admin = Admin.query.filter_by(username_admin=username).first()
        existing_user = User.query.filter_by(username=username).first()

        if existing_admin and check_password_hash(existing_admin.password_hash, password):
            login_user(existing_admin)
            flash('Admin login successful!', "success")
            return redirect(url_for('main.admin_main'))

        elif existing_user and check_password_hash(existing_user.password_hash, password):
            login_user(existing_user)
            flash("User login successful!", "success")
            return redirect(url_for('main.index'))

        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))
