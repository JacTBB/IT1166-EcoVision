from flask import render_template, request, redirect, url_for
from flask_login import login_required
from app.trading import trading
from app.database import query_data, db
from app.models.Trading import Projects
from app.trading.forms import AddProjectForm, EditProjectForm

@trading.route('/')
def home():
    projects = {}
    projectsData = db.session.query(Projects).all()
    for project in projectsData:
        projects[project.id] = {
            'name': project.name,
            'type': project.type
        }

    return render_template('trading/Dashboard.html', projects = projects)


@trading.route('/project/<project>')
def project(project):
    projectData = Projects.query.get(project)
    return render_template('trading/Project.html', project=projectData)

@trading.route("/projects")
@login_required
def projects():
    projects = {}
    projectsData = db.session.query(Projects).all()
    for project in projectsData:
        projects[project.id] = {
            'name': project.name,
            'type': project.type
        }
    
    return render_template('trading/ProjectF.html', projects=projects)   

@trading.route("/project/add", methods=['GET', 'POST'])
def project_add():
    form = AddProjectForm()

    if form.validate_on_submit():
        try:
            name = request.form.get("name")
            type = request.form.get("type")
            
            project = Projects(name=name, type=type)
            db.session.add(project)
            db.session.commit()
            
            return redirect(url_for('trading.projects'))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()
    
    return render_template('trading/ProjectA.html', form=form)

@trading.route("/project/<project>/edit", methods=['GET', 'POST'])
@login_required
def project_edit(project):
    form = EditProjectForm()
    
    if form.validate_on_submit():
        try:
            projectData = Projects.query.get(project)
            
            name = request.form.get("name")
            type = request.form.get("type")
           
            if name:
                projectData.name = name
            if type:
                projectData.type = type
            
            db.session.commit()
            
            return redirect(url_for('trading.projects'))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()
    
    return render_template('trading/ProjectE.html', form=form)

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