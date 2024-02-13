from flask import render_template, request, redirect, url_for, session, g
from flask_login import login_required
from app.trading import trading
from app.auth import check_user_type
from app.database import query_data, db
from app.email import email_transaction
from sqlalchemy.orm.attributes import flag_modified
from app.models.Company import Company
from app.models.Trading import Projects
from app.models.Client import Location, Utility
from app.models.Transaction import Transaction, CarbonPurchase
from app.trading.forms import AddProjectForm, EditProjectForm, ProjectDetailsForm, AddToCart
from flask_login import current_user
from datetime import datetime
import threading



@trading.before_request
@login_required
def get_company():
    if current_user.type == 'client':
        company = Company.query.get(current_user.company)
        g.company = company
        return

    if not 'company' in session:
        class TempCompany:
            def __init__(self):
                self.name = "Admin"
            
        if request.endpoint == 'trading.projects':
            g.company = TempCompany()
            return
        if request.endpoint == 'trading.project_add':
            g.company = TempCompany()
            return
        if request.endpoint == 'trading.project_edit':
            g.company = TempCompany()
            return
        if request.endpoint == 'trading.project_delete':
            g.company = TempCompany()
            return
        return redirect(url_for('staff.companies'))
        
    company = Company.query.get(session['company'])
    g.company = company



@trading.route('/')
@login_required
def home():
    overview = {
        'totalcarbonfootprint': 0,
        'carbonfootprintoffsetted': 0
    }

    locations = {}
    locationsData = db.session.query(Location).filter_by(company=g.company.id)
    for location in locationsData:
        utilitiesData = db.session.query(Utility).filter_by(company=g.company.id, location=location.id)
        for utility in utilitiesData:
            overview['totalcarbonfootprint'] += float(utility.carbonfootprint)
    
    carbonpurchasesData = db.session.query(CarbonPurchase).filter_by(company=g.company.id)
    for carbonpurchase in carbonpurchasesData:
        overview['carbonfootprintoffsetted'] += carbonpurchase.offset
    
    overview['carbonfootprintexceeded'] = overview['totalcarbonfootprint'] - overview['carbonfootprintoffsetted']
    overview['locations'] = len(locations)
    
    
    
    projects = {}
    projectsData = db.session.query(Projects).all()
    for project in projectsData:
        # typeID, if type = conservetion, id = 1
        # Add typeID to dictionary below
        # use css order for typeID
        # if project.type == "Conservation":
        #     project.typeID = 1
        # elif project.type == "Renewable":
        #     project.typeID = 2
        # else:
        #     project.typeID = 3
        projects[project.id] = {
            'id': project.id,
            'name': project.name,
            'type': project.type,
            'stock': project.stock,
            'price': project.price,
            # 'typeID': project.type
            # ID
        }
    filter_value = request.args.get('category', 'all')

    return render_template('trading/Dashboard.html', overview=overview, projects=projects, filter_value=filter_value)

@trading.route("/about")
@login_required
def about():
    return render_template('trading/AboutCarbon.html')

# @trading.route("/Checkout")
# @login_required
# def Checkout():
#     projects = {}
#     projectsData = db.session.query(Projects).all()
#     for project in projectsData:
#         projects[project.id] = {
#             'name': project.name,
#             'type': project.type,
#             'stock': project.stock,
#             'price': project.price,
#         }

#     cart = {}
#     for item in session['cart']:
#         ID = item["id"]
#         if ID in projects:
#             cart[ID] = {
#                 "id": ID,
#                 "name": projects[ID]['name'],
#                 "type": projects[ID]['type'],
#                 "stock": item['stock'],
#                 "price": projects[ID]['price'],
#                 "total_price" : int(item['stock']) * projects[ID]['price'],
#             }
#         else:
#             session['cart'].remove(item)
        
#     return render_template('trading/ProjectCheckout.html', cart = cart)

# @trading.route("/delete_cart/<cart_id>")
# @login_required
# def remove_cart(cart_id):
#     cart = session['cart']
#     for item in cart:
#         if item['id'] == int(cart_id):  
#             cart.remove(item)
#     session['cart'] = cart
#     return redirect(url_for('trading.Checkout'))

# @trading.route("/add_to_cart/<project>", methods=['POST'])
# @login_required
# def add_to_cart(project):
#     if not 'cart' in session:
#         session['cart'] = []
    
#     cart = session['cart']
#     cart.append({"id": int(project), "stock": request.form.get('stock')})
#     session['cart'] = cart

#     return redirect(url_for("trading.Checkout")) 

@trading.route("/purchase/<project>", methods=['POST'])
@login_required
def purchase(project):
    projectData = Projects.query.get(project)
    
    amount = int(request.form.get("stock"))
    
    company = g.company.id
    name = projectData.name
    date = datetime.now()
    price = projectData.price * amount
    
    projectData.stock = projectData.stock - amount

    transaction = Transaction(company=company, name=f"Carbon Purchase - {name}", date=date, price=price)
    db.session.add(transaction)
    
    carbonpurchase = CarbonPurchase(company=company, name=f"Carbon Purchase - {name}", date=date, offset=amount)
    db.session.add(carbonpurchase)
    
    db.session.commit()
    
    
    
    thread = threading.Thread(target=email_transaction, args=(g.company.email, current_user.username, price, f"Carbon Purchase - {name}"))
    thread.start()
    
    return redirect(url_for("trading.home")) 

@trading.route('/project/<project>', methods=['GET', 'POST'])
@login_required
def project(project):
    form = ProjectDetailsForm()
    formCart = AddToCart()
    projectData = Projects.query.get(project)

    if current_user.is_authenticated and (current_user.type == 'admin'):
        if form.validate_on_submit():
            try:
                post = projectData
                post.content = request.form.get("content")
                print(post.content)

                db.session.add(post)
                db.session.commit()
                status_message = "Article updated successfully!"
            except Exception as e:
                status_message = "Failed to update article! Contact Administrator."
                print(f"Error occurred: {e}")
                db.session.rollback()
    
    projects = {}
    projectsData = db.session.query(Projects).all()
    for project in projectsData:
        projects[project.id] = {
            'id': project.id,
            'name': project.name,
            'type': project.type,
            'stock': project.stock,
            'price': project.price,
        }
    
    return render_template('trading/Project.html', form=form, formCart=formCart, project=projectData, projects=projects)

@trading.route('/project/<project>/addimg', methods=['POST'])
@login_required
def project_addimg(project):
    projectData = Projects.query.get(project)
    
    url = request.form.get("imageUrl")
    print(url)

    if url:
        projectData.carousel.append(url)
        flag_modified(projectData, 'carousel')
        db.session.commit()
    
    return redirect(url_for('trading.project', project=project))

@trading.route("/projects")
@login_required
@check_user_type(['admin', 'manager', 'consultant'])
def projects():
    projects = {}
    projectsData = db.session.query(Projects).all()
    for project in projectsData:
        projects[project.id] = {
            'name': project.name,
            'type': project.type,
            'stock': project.stock,
            'price': project.price,
        }
    
    return render_template('trading/ProjectF.html', projects=projects)   

@trading.route("/project/add", methods=['GET', 'POST'])
@login_required
@check_user_type(['admin', 'manager', 'consultant'])
def project_add():
    form = AddProjectForm()

    if form.validate_on_submit():
        try:
            name = request.form.get("name")
            type = request.form.get("type")
            stock = request.form.get("stock")
            price = request.form.get('price')
            
            project = Projects(name=name, type=type, stock=stock, price=price)
            db.session.add(project)
            db.session.commit()
            
            return redirect(url_for('trading.projects'))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()
    
    return render_template('trading/ProjectAdd.html', form=form)

@trading.route("/project/<project>/edit", methods=['GET', 'POST'])
@login_required
@check_user_type(['admin', 'manager', 'consultant'])
def project_edit(project):
    form = EditProjectForm()
    
    if form.validate_on_submit():
        try:
            projectData = Projects.query.get(project)
            
            name = request.form.get("name")
            type = request.form.get("type")
            stock = request.form.get("stock")
            price = request.form.get("price")
           
            if name:
                projectData.name = name
            if type:
                projectData.type = type
            if stock:
                projectData.stock = stock
            if price:
                projectData.price = price
            
            db.session.commit()
            
            return redirect(url_for('trading.projects'))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()
    
    return render_template('trading/ProjectEdit.html', form=form)

@trading.route("/project/<project>/delete")
@login_required
@check_user_type(['admin', 'manager', 'consultant'])
def project_delete(project):
    try:
        projectData = Projects.query.get(project)
        
        if projectData is None:
            return "Projects Not Found!"
        
        db.session.delete(projectData)
        db.session.commit()
        return redirect(url_for('trading.projects'))
    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
        return "Error"