from flask import render_template, request, redirect, url_for
from app.staff import staff
from app.database import db
from flask_login import login_required



@staff.route("/")
@login_required
def dashboard():
    return render_template("staff/dashboard.html")