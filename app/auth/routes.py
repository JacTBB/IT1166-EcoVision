from flask import render_template, request, redirect, url_for, session
from app.auth import auth
from app.database import db, query_data
from flask_login import current_user, login_required, login_user, logout_user
from app.models.User import Client, Author, Technician, Consultant, Manager, Admin
from app.auth.forms import LoginForm, AddUserForm, EditUserForm



UserList = {'client': Client, 'author': Author,
            'technician': Technician, 'consultant': Consultant,
            'manager': Manager, 'admin': Admin}



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
                    if user.type == 'client':
                        return redirect(url_for('client.dashboard'))
                    else:
                        return redirect(url_for('staff.dashboard'))
                else:
                    error_message = "Invalid password"
            else:
                error_message = "Invalid username"

            db.session.commit()
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

    return render_template("auth/login.html", form=form, error_message=error_message)



@auth.route("/users/<type>")
@login_required
def users(type):
    users = {}
    usersData = db.session.query(UserList[type]).all()
    for user in usersData:
        userData = {
            'username': user.username
        }
        if type == 'client':
            userData['companyID'] = user.company
        users[user.id] = userData
    
    return render_template('auth/users.html', type=type, users=users)



@auth.route("/users/<type>/add", methods=['GET', 'POST'])
@login_required
def user_add(type):
    form = AddUserForm()
    
    if form.validate_on_submit():
        try:
            username = request.form.get("username")
            
            user = UserList[type](username=username)
            user.set_password('123')
            db.session.add(user)
            db.session.commit()
            
            # TODO: Client Company Add, Edit Forms
            
            return redirect(url_for('auth.users', type=type))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()
    
    return render_template("auth/users_add.html", form=form)



@auth.route("/users/<type>/edit/<user>", methods=['GET', 'POST'])
@login_required
def user_edit(type, user):
    form = EditUserForm()
    
    if request.method == 'POST':
        try:
            userData = UserList[type].query.get(user)
            
            username = request.form.get("username")
           
            if username:
                userData.username = username
            
            db.session.commit()
            
            return redirect(url_for('auth.users', type=type))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()
    
    return render_template("auth/users_edit.html", form=form)



@auth.route("/users/<type>/delete/<user>")
@login_required
def user_delete(type, user):
    try:
        userData = UserList[type].query.get(user)
        
        if userData is None:
            return "User Not Found!"
        
        db.session.delete(userData)
        db.session.commit()
        return redirect(url_for('auth.users', type=type))
    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
        return "Error"



@auth.route("/account")
@login_required
def account():
    if current_user.type == "client":
        return redirect(url_for('client.account'))
    return render_template("auth/account.html")



@auth.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('auth.login'))
