from flask import Blueprint, render_template, flash, url_for, request, redirect, request
from .models import User
from . import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods= ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            #if user exists, check hashed password against typed in password
            if check_password_hash(user.password, password):
                flash("logged in!", category= 'success')
                login_user(user, remember=True) #login manager
                return redirect(url_for('views.profile'))
            else:
                flash('Password is incorrect', category= 'error')
                return redirect(url_for('auth.login'))
        else:
            flash('Email/User does not exist', category="error")
            return redirect(url_for('auth.login'))
    else:
        return render_template('auth/login.html', user= current_user)

@auth.route('/signup', methods= ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        email = request.form.get("email")

        # if this returns a user, then the email already exists in database
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email is already in use', category="error")
        elif username_exists:
            flash('Username is already in use', category="error")
        elif password1!=password2:
            flash('Password don\'t match!', category='error')
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        elif len(password1) <6:
            flash('Password is too short', category='error')
        elif len(email) < 4:
            flash('Email is invalid', category='error')
        else:
            new_user = User(email = email, username=username,
                            password = generate_password_hash(password1, method= 'sha256'))
            db.session.add(new_user) #adds to staging area of db
            db.session.commit() #actually adds to db
            login_user(new_user, remember=True) #logs in the user
            flash('User created!')
            return redirect(url_for('views.index'))
        return redirect(url_for('auth.login'))
    else:
        return render_template('/auth/signup.html', user= current_user)

@auth.route('/logout')
@login_required #can only access this page if logged in
def logout():
    flash('Logged out', category='success')
    logout_user()
    return redirect(url_for("views.index"))