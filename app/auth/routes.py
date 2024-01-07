from flask import render_template, request, redirect, url_for
from app.auth import auth
from app.database import db, query_data
from flask_login import current_user, login_required, login_user, logout_user
from app.models.User import Client, Author, Technician, Consultant, Manager, Admin
from app.auth.forms import LoginForm



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.account'))
    
    form = LoginForm()
    error_message = None

    if form.validate_on_submit():
        try:
            username = request.form.get("username")
            password = request.form.get("password")
            
            user = (query_data(Client, filter_by={'username': username}, all=False) or
                    query_data(Author, filter_by={'username': username}, all=False) or
                    query_data(Technician, filter_by={'username': username}, all=False) or
                    query_data(Consultant, filter_by={'username': username}, all=False) or
                    query_data(Manager, filter_by={'username': username}, all=False) or
                    query_data(Admin, filter_by={'username': username}, all=False))
                
            if user:
                if user.username == username and user.check_password(password):
                    login_user(user)
                    if user.type == 'admin':
                        return redirect(url_for('main.news'))
                    return redirect(url_for('auth.account'))
                else:
                    error_message = "Invalid password"
            else:
                error_message = "Invalid username"

            db.session.commit()
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

    return render_template("auth/login.html", form=form, error_message=error_message)



@auth.route("/account")
@login_required
def account():
    username = current_user.username
    return render_template("auth/account.html")



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))