from flask import render_template, request, redirect, url_for
from flask_login import login_remembered, login_required
from app.trading import trading
from app.database import query_data, db


@trading.route('/')
def home():
    return 'This is my trading platform'