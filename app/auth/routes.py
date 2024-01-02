from flask import render_template, session
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