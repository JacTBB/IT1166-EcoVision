from flask import render_template, request, redirect, url_for, abort, flash
from app.models.Contact import CompanyInfo
from app.models.Company import Company
from app.staff import staff
from app.database import db
from app.email import email_transaction
from flask_login import current_user, login_required
from app.auth import check_user_type
from app.models.Inventory import Product
from app.models.Transaction import Transaction
from app.models.Staff import Announcement, Task
from app.models.Chats import Chat
from app.models.User import Author, Technician, Consultant, Manager, Admin
from app.staff.forms import AddProductForm, EditProductForm, AddCompanyInfo, EditCompanyInfo, AnnouncementForm, AddTransactionForm, AddTaskForm
from app.client.accountforms import UpdatePersonalForm, ChangePasswordForm
from app.models.User import Author, Technician, Consultant, Manager, Admin
from datetime import datetime
from string import ascii_lowercase
import random
import os
import threading
from app import socketio



UserList = {'author': Author,
            'technician': Technician, 'consultant': Consultant,
            'manager': Manager, 'admin': Admin}



@staff.route("/", methods=['GET','POST'])
@login_required
@check_user_type(['admin', 'manager', 'consultant', 'technician', 'author'])
def dashboard():
    announcement = {
        'description': "No Announcements.",
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    announcementData = db.session.query(Announcement).first()
    if announcementData:
        announcement['description'] = announcementData.description
        announcement['date'] = announcementData.date.strftime("%Y-%m-%d %H:%M:%S")
        
    announcementForm = AnnouncementForm()
    
    if announcementForm.validate_on_submit():
        try:
            description = request.form.get("description")
            date = datetime.now()
            
            announcementData = db.session.query(Announcement).first()
            if announcementData:
                announcementData.description = description
                announcementData.date = date
                db.session.commit()
            else:
                announcement = Announcement(description=description, date=date)
                db.session.add(announcement)
                db.session.commit()
            
            socketio.emit('announcements', {'description':description, 'date':str(date)})

            return redirect(url_for('staff.dashboard'))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()
    
    tasksData = db.session.query(Task).all()
    
    return render_template("staff/dashboard.html", announcement=announcement, announcementForm=announcementForm, tasks=tasksData)



@staff.route('/task/add', methods=["GET", "POST"])
@login_required
@check_user_type(['admin', 'manager'])
def task_add():
    users = {}
    users_list = []
    
    for UserType in UserList:
        UserClass = UserList[UserType]
            
        usersData = db.session.query(UserClass).all()
        for user in usersData:
            users_list.append(f"{user.type}-{user.username}")
            users[f"{user.type}-{user.username}"] = {
                'type': user.type,
                'id': user.id,
                'username': user.username
            }
    
    
    form = AddTaskForm()
    
    form.user_id.choices = users_list

    if form.validate_on_submit():
        try:
            user = request.form.get("user_id")
            description = request.form.get("description")
            
            userData = users[user]
            user_id = userData['id']
            user_username = userData['username']
            user_type = userData['type']

            task = Task(user_id=user_id, user_username=user_username, user_type=user_type, description=description)
            db.session.add(task)
            db.session.commit()

            return redirect(url_for('staff.dashboard'))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

    return render_template("staff/task_add.html", form=form)



@staff.route('/task/<task>/delete', methods=["GET", "POST"])
@login_required
@check_user_type(['admin', 'manager'])
def task_delete(task):
    task = Task.query.get(task)
    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('staff.dashboard'))






@staff.route("/products")
@login_required
@check_user_type(['admin', 'manager', 'technician'])
def products():
    products = {}
    productsData = db.session.query(Product).all()
    for product in productsData:
        products[product.id] = {
            'name': product.name,
            'quantity': product.quantity
        }

    return render_template('staff/inventory.html', products=products)


@staff.route("/product/add", methods=['GET', 'POST'])
@login_required
@check_user_type(['admin', 'manager'])
def product_add():
    form = AddProductForm()

    if form.validate_on_submit():
        try:
            name = request.form.get("name")
            quantity = request.form.get("quantity")

            product = Product(name=name, quantity=quantity)
            db.session.add(product)
            db.session.commit()

            return redirect(url_for('staff.products'))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

    return render_template("staff/inventory_add.html", form=form)


@staff.route("/product/<product>/edit", methods=['GET', 'POST'])
@login_required
@check_user_type(['admin', 'manager'])
def product_edit(product):
    form = EditProductForm()

    if request.method == 'POST':
        try:
            productData = Product.query.get(product)

            name = request.form.get("name")
            quantity = request.form.get("quantity")

            if name:
                productData.name = name
            if quantity:
                productData.quantity = quantity

            db.session.commit()

            return redirect(url_for('staff.products'))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

    return render_template("staff/inventory_edit.html", form=form)


@staff.route("/product/<product>/delete")
@login_required
@check_user_type(['admin', 'manager'])
def product_delete(product):
    try:
        productData = Product.query.get(product)

        if productData is None:
            return "Product Not Found!"

        db.session.delete(productData)
        db.session.commit()
        return redirect(url_for('staff.products'))
    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
        return "Error"
    


@staff.route("/companies")
@login_required
@check_user_type(['admin', 'manager', 'consultant'])
def companies():
    companies = {}
    companiesData = db.session.query(Company).all()
    for company in companiesData:
        companies[company.id] = {
            'name': company.name,
            'industry': company.industry,
            'address': company.address,
            'email': company.email,
            'plan': company.plan
        }

    return render_template('staff/companies.html', companies=companies)



@staff.route("/enquiries")
@login_required
@check_user_type(['admin', 'manager', 'consultant'])
def enquiries():
    try:
        data = CompanyInfo.query.all()
        return render_template("staff/enquiries.html", data=data)
    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
        return "Error"


@staff.route("/enquiries/<enquiry>/delete")
@login_required
@check_user_type(['admin', 'manager'])
def enquiry_delete(enquiry):
    try:
        enquiryData = CompanyInfo.query.get(enquiry)

        if enquiryData is None:
            return "Enquiry Not Found!"

        db.session.delete(enquiryData)
        db.session.commit()
        return redirect(url_for('staff.enquiries'))
    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
        return "Error"


@staff.route("/enquiries/<enquiry>/edit", methods=['GET', 'POST'])
@login_required
@check_user_type(['admin', 'manager'])
def enquiry_edit(enquiry):
    enquiryData = CompanyInfo.query.get(enquiry)
    form = EditCompanyInfo(obj=enquiryData)
    if request.method == 'POST':
        try:

            name = request.form.get("name")
            email = request.form.get("email")
            message = request.form.get("message")

            if name:
                enquiryData.name = name
            if email:
                enquiryData.email = email
            if message:
                enquiryData.message = message

            db.session.commit()

            return redirect(url_for('staff.enquiries'))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

    return render_template("staff/enquiries_edit.html", form=form)



@staff.route('/chat')
def chats_staff():
    company = 0
    
    chatData = db.session.query(Chat).filter_by(company=company).first()
    if not chatData:
        chatData = Chat(company=company,messages=[])
        db.session.add(chatData)
        db.session.commit()
    
    messages = []
    for message in chatData.messages:
        time = datetime.fromtimestamp(message['timestamp']/1000)
        msg = {
            'username': message['username'],
            'timestamp': time.strftime("%b %d, %Y, %r"),
            'message': message['message']
        }
        messages.append(msg)
    
    return render_template('staff/chat.html', room=chatData.id, messages=messages)







@staff.route("/account")
@login_required
@check_user_type(['admin', 'manager', 'consultant', 'technician', 'author'])
def account():
    form1 = UpdatePersonalForm()
    form1.first_name.data = current_user.first_name
    form1.last_name.data = current_user.last_name
    form1.username.data = current_user.username
    form1.email.data = current_user.email
    form1.phone_number.data = current_user.phone_number
    form1.profile_picture.data = current_user.profile_picture
    
    form2 = ChangePasswordForm()
    
    return render_template("staff/account.html", form1=form1, form2=form2)



@staff.route("/account/update/personal", methods=["POST"])
@login_required
@check_user_type(['admin', 'manager', 'consultant', 'technician', 'author'])
def account_update_personal():
    form = UpdatePersonalForm()
    
    if form.validate_on_submit():
        try:
            userData = UserList[current_user.type].query.get(current_user.id)
            
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            username = request.form.get("username")
            email = request.form.get("email")
            phone_number = request.form.get("phone_number")
            
            profile_pictue = form.profile_picture.data
            profile_pictue_filename = "uploads/profile-"
            for i in range(10):
                profile_pictue_filename += random.choice(ascii_lowercase)
            profile_pictue.save(os.path.join(
                './app/static/images', f'{profile_pictue_filename}'
            ))
            
            userData.first_name = first_name
            userData.last_name = last_name
            userData.username = username
            userData.email = email
            userData.phone_number = phone_number
            userData.profile_picture = profile_pictue_filename

            db.session.commit()
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()
    else:
        flash("Personal Profile Validation Error!")
        for input in form:
            if input.errors:
                flash(f'\n{input.name} - {input.errors[0]}')

    return redirect(url_for('staff.account'))



@staff.route("/account/update/password", methods=["POST"])
@login_required
@check_user_type(['admin', 'manager', 'consultant', 'technician', 'author'])
def account_update_password():
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        try:
            userData = UserList[current_user.type].query.get(current_user.id)
            
            password = request.form.get("password")
            userData.set_password(password)

            db.session.commit()
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()
    else:
        flash("Change Password Validation Error!")
        for input in form:
            if input.errors:
                flash(f'\n{input.name} - {input.errors[0]}')

    return redirect(url_for('staff.account'))