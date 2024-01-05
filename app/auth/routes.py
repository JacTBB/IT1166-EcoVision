from flask import render_template, request, redirect, url_for
from app.auth import auth
from app.database import db, query_data
from flask_login import current_user, login_required, login_user, logout_user
from app.models.User import Customer, Admin
from app.auth.forms import LoginForm



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.account'))
    
    form = LoginForm()
    error_message = None
    admin = request.args.get('admin')
    requestAdminLogin = False
    if admin is not None:
        requestAdminLogin = True

    if form.validate_on_submit():
        try:
            username = request.form.get("username")
            password = request.form.get("password")
            
            if requestAdminLogin == True:
                user = query_data(Admin, filter_by={'username': username}, all=False)
                print(user)
                
                if user:
                    if user.username == username and user.check_password(password):
                        login_user(user)
                        return redirect(url_for('auth.account'))
                    else:
                        error_message = "Invalid password"
                else:
                    error_message = "Invalid username"
            else:
                user = query_data(Customer, filter_by={'username': username}, all=False)
                print(user)
                
                if user:
                    if user.username == username and user.check_password(password):
                        login_user(user)
                        return redirect(url_for('auth.account'))
                    else:
                        error_message = "Invalid password"
                else:
                    error_message = "Invalid username"

            db.session.commit()
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

    return render_template("login.html", form=form, error_message=error_message, requestAdminLogin=requestAdminLogin)



@auth.route("/account")
@login_required
def account():
    username = current_user.username
    print(current_user)
    return render_template("account.html", username=username)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))