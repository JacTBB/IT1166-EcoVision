from flask import render_template, redirect, url_for
from app.auth import auth
from app.database import db
from flask_login import LoginManager, current_user, login_required, login_user, logout_user



@auth.route('/login')
def login():
    return "Login"

@auth.route("/protected")
@login_required
def protected():
    if current_user.is_authenticated:
        username = current_user.username
    else:
        username = "Guest"
    return f"Logged in as: {username}"

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))