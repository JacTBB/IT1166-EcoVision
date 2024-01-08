from flask import render_template, request, redirect, url_for
from app.staff import staff
from app.database import db
from flask_login import login_required
from app.models.Inventory import Product
from app.staff.forms import AddProductForm, EditProductForm



@staff.route("/")
@login_required
def dashboard():
    return render_template("staff/dashboard.html")



@staff.route("/products")
@login_required
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