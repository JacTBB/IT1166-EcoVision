from flask import render_template, request, redirect, url_for, abort
from app.models.Contact import CompanyInfo
from app.models.Company import Company
from app.staff import staff
from app.database import db
from flask_login import current_user, login_required
from app.auth import check_user_type
from app.models.Inventory import Product
from app.staff.forms import AddProductForm, EditProductForm, AddCompanyInfo, EditCompanyInfo


@staff.route("/")
@login_required
@check_user_type(['admin', 'manager', 'consultant', 'technician', 'author'])
def dashboard():
    return render_template("staff/dashboard.html")


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

@staff.route('/staff/chats')
def chats():
    return render_template('main/room/staffchat.html')  

