from flask import render_template, request
from app.client import client
from app.database import db
from flask_login import login_required



@client.route('/')
@login_required
def dashboard():
    return render_template('client/dashboard.html')

@client.route("/account")
@login_required
def account():
    return render_template("client/account.html")