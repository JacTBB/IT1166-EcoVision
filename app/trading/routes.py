from flask import render_template, request, redirect, url_for, session, g
from flask_login import login_required
from app.trading import trading
from app.database import query_data, db
from app.models.Company import Company
from app.models.Trading import Projects
from app.trading.forms import AddProjectForm, EditProjectForm, ProjectDetailsForm, AddToCart
from flask_login import current_user



@trading.before_request
@login_required
def get_company():
    if current_user.type == 'client':
        company = Company.query.get(current_user.company)
        g.company = company
        return
    
    if not 'company' in session:
        if request.endpoint == 'client.company_view':
            return
        return redirect(url_for('staff.companies'))
        
    company = Company.query.get(session['company'])
    g.company = company



@trading.route('/')
def home():
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
            'name': project.name,
            'type': project.type,
            'stock': project.stock,
            'price': project.price,
            # 'typeID': project.typeID
        }

    return render_template('trading/Dashboard.html', projects = projects)

@trading.route("/about")
def about():
    return render_template('trading/AboutCarbon.html')

@trading.route("/Checkout")
@login_required
def Checkout():
    projects = {}
    projectsData = db.session.query(Projects).all()
    for project in projectsData:
        projects[project.id] = {
            'name': project.name,
            'type': project.type,
            'stock': project.stock,
            'price': project.price,
        }

    print(projects)
    print(session['cart'])

    cart = {}
    for item in session['cart']:
        ID = item["id"]
        if ID in projects:
            cart[ID] = {
                "id": ID,
                "name": projects[ID]['name'],
                "type": projects[ID]['type'],
                "stock": item['stock'],
                "price": projects[ID]['price'],
                "total_price" : int(item['stock']) * projects[ID]['price'],
            }
        else:
            session['cart'].remove(item)
        
    return render_template('trading/ProjectCheckout.html', cart = cart)

@trading.route("/delete_cart/<cart_id>")
def remove_cart(cart_id):
    cart = session['cart']
    for item in cart:
        if item['id'] == int(cart_id):  
            cart.remove(item)
    session['cart'] = cart
    return redirect(url_for('trading.Checkout'))

@trading.route("/add_to_cart/<project>", methods=['POST'])
def add_to_cart(project):
    if not 'cart' in session:
        session['cart'] = []
    
    cart = session['cart']
    cart.append({"id": int(project), "stock": request.form.get('stock')})
    session['cart'] = cart

    return redirect(url_for("trading.Checkout")) 

@trading.route('/project/<project>', methods=['GET', 'POST'])
def project(project):
    form = ProjectDetailsForm()
    formCart = AddToCart()
    projectData = Projects.query.get(project)

    if current_user.is_authenticated and (current_user.type == 'admin'):
        if request.method == 'POST':
            if form.validate_on_submit():
                if request.form.get('csrf_token'):
                    try:
                        post = projectData
                        post.content = form.content.data

                        db.session.add(post)
                        db.session.commit()
                        status_message = "Article updated successfully!"
                    except Exception as e:
                        status_message = "Failed to update article! Contact Administrator."
                        print(f"Error occurred: {e}")
                        db.session.rollback()
                        
    return render_template('trading/Project.html', form=form, formCart=formCart, project=projectData)

@trading.route("/projects")
@login_required
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