from flask import render_template, request, redirect, url_for, session, g
from app.client import client
from app.database import db
from flask_login import login_required, current_user
from app.auth import check_user_type
from app.models.Client import Location, Utility, Assessment
from app.models.Company import Company
from app.client.forms import AddCompanyForm, EditCompanyForm, AddLocationForm, EditLocationForm, AddUtilityForm, EditUtilityForm, AddAssessmentForm, EditAssessmentForm
from datetime import datetime



@client.before_request
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



@client.route('/')
@login_required
def dashboard():
    overview = {
        'carbonfootprint': 100,
        'energyusage': 100,
        'waterusage': 100,
    }

    locations = {}
    locationsData = db.session.query(Location).filter_by(company=g.company.id)
    for location in locationsData:
        utilities = {
            'timerange': [],
            'carbonfootprint': [],
            'energyusage': [],
            'waterusage': []
        }
        
        utilitiesData = db.session.query(Utility).filter_by(company=g.company.id, location=location.id)
        for utility in utilitiesData:
            utilities['timerange'].append(int(datetime(utility.date.year, utility.date.month, utility.date.day).timestamp()))
            utilities['carbonfootprint'].append(int(utility.carbonfootprint))
            utilities['energyusage'].append(int(utility.energyusage))
            utilities['waterusage'].append(int(utility.waterusage))
            
        locations[location.id] = {
            'name': location.name,
            'timerange': utilities["timerange"],
            'carbonfootprint': utilities['carbonfootprint'],
            'energyusage': utilities['energyusage'],
            'waterusage': utilities['energyusage']
        }

    if g.company.plan == 'free':
        return render_template('client/dashboard_free.html', overview=overview, locations=locations)
    
    
    
    overview['carbonfootprintexceeded'] = 50
    overview['carbonfootprintoffsetted'] = 200
    overview['notifications'] = 10
    overview['locations'] = 10
    
    assessments = {}
    assessmentsData = db.session.query(Assessment).filter_by(company=g.company.id)
    for assessment in assessmentsData:
        assessments[assessment.id] = {
            'location': assessment.location,
            'name': assessment.name,
            'type': assessment.type,
            'progress': assessment.progress
        }
    
    return render_template('client/dashboard_custom.html', overview=overview, assessments=assessments, locations=locations)



@client.route("/company/<company>")
@login_required
@check_user_type(['admin', 'manager', 'consultant'])
def company_view(company):
    print('CV', company)
    session['company'] = company
    print(session['company'])
    
    return redirect(url_for('client.dashboard'))






@client.route("/manage")
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

    return render_template('client/companies.html', companies=companies)



@client.route("/manage/add", methods=['GET', 'POST'])
@login_required
@check_user_type(['admin', 'manager'])
def company_add():
    form = AddCompanyForm()

    if form.validate_on_submit():
        try:
            name = request.form.get("name")
            industry = request.form.get("industry")
            address = request.form.get("address")
            email = request.form.get("email")
            plan = request.form.get("plan")

            company = Company(name=name, industry=industry, address=address, email=email, plan=plan)
            db.session.add(company)
            db.session.commit()

            return redirect(url_for('client.companies'))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

    return render_template("client/company_add.html", form=form)



@client.route("/manage/<company>/edit", methods=['GET', 'POST'])
@login_required
@check_user_type(['admin', 'manager'])
def company_edit(company):
    form = EditCompanyForm()

    if request.method == 'POST':
        try:
            companyData = Company.query.get(company)

            name = request.form.get("name")
            industry = request.form.get("industry")
            address = request.form.get("address")
            email = request.form.get("email")
            plan = request.form.get("plan")

            if name:
                companyData.name = name
            if industry:
                companyData.industry = industry
            if address:
                companyData.address = address
            if email:
                companyData.email = email
            if plan:
                companyData.plan = plan

            db.session.commit()

            return redirect(url_for('client.companies'))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

    return render_template("client/company_edit.html", form=form)



@client.route("/manage/<company>/delete")
@login_required
@check_user_type(['admin', 'manager'])
def company_delete(company):
    try:
        companyData = Location.query.get(company)

        if companyData is None:
            return "Company Not Found!"

        db.session.delete(companyData)
        db.session.commit()
        return redirect(url_for('client.companies'))
    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
        return "Error"






@client.route("/locations")
@login_required
def locations():
    locations = {}
    locationsData = db.session.query(Location).filter_by(company=g.company.id)
    for location in locationsData:
        locations[location.id] = {
            'name': location.name,
            'address': location.address
        }

    return render_template('client/locations.html', locations=locations)



@client.route("/location/add", methods=['GET', 'POST'])
@login_required
def location_add():
    form = AddLocationForm()

    if form.validate_on_submit():
        try:
            name = request.form.get("name")
            address = request.form.get("address")

            location = Location(name=name, address=address)
            db.session.add(location)
            db.session.commit()

            return redirect(url_for('client.locations'))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

    return render_template("client/location_add.html", form=form)



@client.route("/location/<location>/edit", methods=['GET', 'POST'])
@login_required
def location_edit(location):
    form = EditLocationForm()

    if request.method == 'POST':
        try:
            locationData = Location.query.get(location)

            name = request.form.get("name")
            address = request.form.get("address")

            if name:
                locationData.name = name
            if address:
                locationData.address = address

            db.session.commit()

            return redirect(url_for('client.locations'))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

    return render_template("client/location_edit.html", form=form)



@client.route("/location/<location>/delete")
@login_required
def location_delete(location):
    try:
        locationData = Location.query.get(location)

        if locationData is None:
            return "Location Not Found!"

        db.session.delete(locationData)
        db.session.commit()
        return redirect(url_for('client.locations'))
    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
        return "Error"






@client.route("/location/<location>/utility")
@login_required
def location_utility(location):
    utilities = {}
    utilitiesData = db.session.query(Utility).filter_by(company=g.company.id, location=int(location))
    for utility in utilitiesData:
        utilities[utility.id] = {
            'name': utility.name,
            'date': utility.date,
            'carbonfootprint': utility.carbonfootprint,
            'energyusage': utility.energyusage,
            'waterusage': utility.waterusage
        }

    return render_template('client/utility.html', location=location, utilities=utilities)



@client.route("/location/<location>/utility/add", methods=['GET', 'POST'])
@login_required
def location_utility_add(location):
    form = AddUtilityForm()
    
    # TODO: Improve perms checker, only clients can edit utilities in their company & location

    if form.validate_on_submit():
        try:
            name = request.form.get("name")
            date = datetime.strptime(
                request.form.get("date"), "%Y-%m-%d").date()
            carbonfootprint = request.form.get("carbonfootprint")
            energyusage = request.form.get("energyusage")
            waterusage = request.form.get("waterusage")

            utility = Utility(location=location, name=name, date=date,
                              carbonfootprint=carbonfootprint, energyusage=energyusage, waterusage=waterusage)
            db.session.add(utility)
            db.session.commit()

            return redirect(url_for('client.location_utility', location=location))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

    return render_template("client/utility_add.html", form=form)



@client.route("/location/<location>/utility/edit/<utility>", methods=['GET', 'POST'])
@login_required
def location_utility_edit(location, utility):
    form = EditUtilityForm()

    if request.method == 'POST':
        try:
            utilityData = Utility.query.get(utility)

            name = request.form.get("name")
            date = request.form.get("date")
            carbonfootprint = request.form.get("carbonfootprint")
            energyusage = request.form.get("energyusage")
            waterusage = request.form.get("waterusage")

            if name:
                utilityData.name = name
            if date:
                utilityData.date = datetime.strptime(date, "%Y-%m-%d").date()
            if carbonfootprint:
                utilityData.carbonfootprint = carbonfootprint
            if energyusage:
                utilityData.energyusage = energyusage
            if waterusage:
                utilityData.waterusage = waterusage

            db.session.commit()

            return redirect(url_for('client.location_utility', location=location))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

    return render_template("client/utility_edit.html", form=form)



@client.route("/location/<location>/utility/delete/<utility>")
@login_required
def location_utility_delete(location, utility):
    try:
        utilityData = Utility.query.get(utility)

        if utilityData is None:
            return "Utility Not Found!"

        db.session.delete(utilityData)
        db.session.commit()
        return redirect(url_for('client.location_utility', location=location))
    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
        return "Error"






@client.route("/assessments")
@login_required
def assessments():
    assessments = {}
    assessmentsData = db.session.query(Assessment).filter_by(company=g.company.id)
    for assessment in assessmentsData:
        assessments[assessment.id] = {
            'location': assessment.location,
            'name': assessment.name,
            'type': assessment.type,
            'progress': assessment.progress
        }

    return render_template('client/assessments.html', assessments=assessments)



@client.route("/assessment/add", methods=['GET', 'POST'])
@login_required
def assessment_add():
    form = AddAssessmentForm()

    if form.validate_on_submit():
        try:
            location = request.form.get("location")
            name = request.form.get("name")
            type = request.form.get("type")
            progress = request.form.get("progress")

            assessment = Assessment(company=g.company.id, location=location, name=name, type=type, progress=progress)
            db.session.add(assessment)
            db.session.commit()

            return redirect(url_for('client.assessments'))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

    return render_template("client/assessment_add.html", form=form)



@client.route("/assessment/<assessment>/edit", methods=['GET', 'POST'])
@login_required
def assessment_edit(assessment):
    form = EditAssessmentForm()

    if request.method == 'POST':
        try:
            assessmentData = Assessment.query.get(assessment)

            location = request.form.get("location")
            name = request.form.get("name")
            type = request.form.get("type")
            progress = request.form.get("progress")

            if location:
                assessmentData.location = location
            if name:
                assessmentData.name = name
            if type:
                assessmentData.type = type
            if progress:
                assessmentData.progress = progress

            db.session.commit()

            return redirect(url_for('client.assessments'))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

    return render_template("client/assessment_edit.html", form=form)



@client.route("/assessment/<assessment>/delete")
@login_required
def assessment_delete(assessment):
    try:
        assessmentData = Assessment.query.get(assessment)

        if assessmentData is None:
            return "Assessment Not Found!"

        db.session.delete(assessmentData)
        db.session.commit()
        return redirect(url_for('client.assessments'))
    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
        return "Error"






@client.route("/account")
@login_required
def account():
    if current_user.type != 'client':
        return redirect(url_for('auth.account'))
    return render_template("client/account.html")