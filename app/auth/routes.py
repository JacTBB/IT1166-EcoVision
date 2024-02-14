from flask import render_template, request, redirect, url_for, session, flash
from app.auth import auth, check_user_type
from app.database import db, query_data
from app.email import email_register, email_recovery
from flask_login import current_user, login_required, login_user, logout_user
from app.models.User import Client, Author, Technician, Consultant, Manager, Admin
from app.models.Company import Company
from app.auth.forms import LoginForm, RegisterForm, AddUserForm, EditUserForm, RecoveryForm
import threading
import uuid


UserList = {'client': Client, 'author': Author,
            'technician': Technician, 'consultant': Consultant,
            'manager': Manager, 'admin': Admin}



RecoveryList = {}



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


@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.account'))

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            username = request.form.get("username")
            email = request.form.get("email")
            phone_number = request.form.get("phone_number")
            password = request.form.get("password")

            company_name = request.form.get("company_name")
            company_industry = request.form.get("company_industry")
            company_email = request.form.get("company_email")
            company_phone_number = request.form.get("company_phone_number")
            company_address = request.form.get("company_address")
            company_logo = 'icon.jpg'
            company_plan = 'free'

            company = Company(name=company_name, industry=company_industry, email=company_email,
                              phone_number=company_phone_number, address=company_address, logo=company_logo, plan=company_plan)
            db.session.add(company)
            db.session.commit()

            client = Client(username=username, email=email)
            client.first_name = first_name
            client.last_name = last_name
            client.phone_number = phone_number
            client.set_password(password)
            client.set_company(company.id)
            db.session.add(client)
            db.session.commit()
            
            thread = threading.Thread(target=email_register, args=(email, username))
            thread.start()

            return redirect(url_for('auth.login'))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()
            flash("Register Validation Error!")
            for input in form:
                if input.errors:
                    flash(f'\n{input.name} - {input.errors[0]}')

    return render_template('auth/register.html', form=form)


@auth.route('/recovery', methods=['GET', 'POST'])
def recovery():
    if current_user.is_authenticated:
        return redirect(url_for('auth.account'))

    form = RecoveryForm()
    error_message = None
    recovery_message = None

    if form.validate_on_submit():
        try:
            email = request.form.get("email")

            user = (query_data(Client, filter_by={'email': email}, all=False) or
                    query_data(Author, filter_by={'email': email}, all=False) or
                    query_data(Technician, filter_by={'email': email}, all=False) or
                    query_data(Consultant, filter_by={'email': email}, all=False) or
                    query_data(Manager, filter_by={'email': email}, all=False) or
                    query_data(Admin, filter_by={'email': email}, all=False))

            if user:
                RecoveryID = uuid.uuid4()
                
                RecoveryList[str(RecoveryID)] = user.email
                
                Recovery = url_for('auth.recoveryid', id=RecoveryID, _external=True)
                
                thread = threading.Thread(target=email_recovery, args=(email, user.username, Recovery))
                thread.start()
                
                recovery_message = 'Recovery Email Sent!'
            else:
                error_message = "Invalid email"

            db.session.commit()
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

    return render_template("auth/recovery.html", form=form, error_message=error_message, recovery_message=recovery_message)



@auth.route('/recoveryid/<id>', methods=['GET', 'POST'])
def recoveryid(id):
    if id in RecoveryList:
        email = RecoveryList[id]
        
        user = (query_data(Client, filter_by={'email': email}, all=False) or
                    query_data(Author, filter_by={'email': email}, all=False) or
                    query_data(Technician, filter_by={'email': email}, all=False) or
                    query_data(Consultant, filter_by={'email': email}, all=False) or
                    query_data(Manager, filter_by={'email': email}, all=False) or
                    query_data(Admin, filter_by={'email': email}, all=False))
        
        password = str(uuid.uuid4())
        
        user.set_password(password)
        
        flash(f"Your new password is: {password}")
        flash(f"Please change your password once logged in.")
        
        db.session.commit()
        
        RecoveryList[id] = None
        
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('auth.recovery'))






@auth.route("/users")
@login_required
@check_user_type(['admin', 'manager'])
def users_list():
    return render_template('auth/users_list.html')


@auth.route("/users/<type>")
@login_required
@check_user_type(['admin', 'manager'])
def users(type):
    users = {}
    usersData = db.session.query(UserList[type]).all()
    for user in usersData:
        userData = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number,
        }
        if type == 'client':
            userData['companyID'] = user.company
        users[user.id] = userData

    return render_template('auth/users.html', type=type, users=users)


@auth.route("/users/<type>/add", methods=['GET', 'POST'])
@login_required
@check_user_type(['admin', 'manager'])
def user_add(type):
    form = AddUserForm()

    if form.validate_on_submit():
        try:
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            username = request.form.get("username")
            email = request.form.get("email")
            phone_number = request.form.get("phone_number")
            company = request.form.get("company")
            password = request.form.get("password")

            user = UserList[type](username=username, email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.phone_number = phone_number
            user.set_password(password)
            if type == 'client':
                user.set_company(company)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('auth.users', type=type))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

    return render_template("auth/users_add.html", form=form, type=type)


@auth.route("/users/<type>/edit/<user>", methods=['GET', 'POST'])
@login_required
@check_user_type(['admin', 'manager'])
def user_edit(type, user):
    userData = UserList[type].query.get(user)
    
    form = EditUserForm()
    form.first_name.data = userData.first_name
    form.last_name.data = userData.last_name
    form.username.data = userData.username
    form.email.data = userData.email
    form.phone_number.data = userData.phone_number

    if request.method == 'POST':
        try:
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            username = request.form.get("username")
            email = request.form.get("email")
            phone_number = request.form.get("phone_number")
            company = request.form.get("company")

            userData.first_name = first_name
            userData.last_name = last_name
            userData.username = username
            userData.email = email
            userData.phone_number = phone_number
            if type == 'client':
                userData.set_company(company)

            db.session.commit()

            return redirect(url_for('auth.users', type=type))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

    return render_template("auth/users_edit.html", form=form, type=type, company=userData.company)


@auth.route("/users/<type>/delete/<user>")
@login_required
@check_user_type(['admin', 'manager'])
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
    return redirect(url_for('staff.account'))


@auth.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('auth.login'))
