from flask import render_template, request, redirect, url_for
from flask_login import login_required
from app.trading import trading
from app.database import query_data, db
from app.models.Trading import Projects
from app.trading.forms import AddProjectForm, EditProjectForm

@trading.route('/')
def home():
    projects = {1: "project 1", 2: "project 2"}

    return render_template('trading/Dashboard.html', projects = projects)


@trading.route('/project/<project>')
def project(project):
    return render_template('trading/ProjectF.html', project = project)

@trading.route("/locations")
@login_required
def locations():
    locations = {}
    locationsData = db.session.query(Projects).all()
    for location in locationsData:
        locations[location.id] = {
            'name': location.name,
            'type': location.type
        }
    
    return render_template('trading/ProjectF.html', locations=locations)   

@trading.route("/project/add", methods=['GET', 'POST'])
def project_add():
    form = AddProjectForm()

    if form.validate_on_submit():
        try:
            name = request.form.get("name")
            type = request.form.get("type")
            
            location = Projects(name=name, type=type)
            db.session.add(location)
            db.session.commit()
            
            return redirect(url_for('trading.locations'))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()
    
    return render_template('trading/ProjectA.html', form=form)

@trading.route("/location/<location>/edit", methods=['GET', 'POST'])
@login_required
def location_edit(location):
    form = EditProjectForm()
    
    if form.validate_on_submit():
        try:
            locationData = Projects.query.get(location)
            
            name = request.form.get("name")
            type = request.form.get("type")
           
            if name:
                locationData.name = name
            if type:
                locationData.type = type
            
            db.session.commit()
            
            return redirect(url_for('trading.locations'))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()
    
    return render_template('trading/ProjectE.html', form=form)

@trading.route("/location/<location>/delete")
@login_required
def location_delete(location):
    try:
        locationData = Projects.query.get(location)
        
        if locationData is None:
            return "Projects Not Found!"
        
        db.session.delete(locationData)
        db.session.commit()
        return redirect(url_for('trading.locations'))
    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
        return "Error"