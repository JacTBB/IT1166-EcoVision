from flask import render_template, request, redirect, url_for, session, g, flash
from app import socketio
from app.client import client
from app.database import db
from app.email import email_transaction, email_upgrade_account
from sqlalchemy.orm.attributes import flag_modified
from flask_login import login_required, current_user
from app.auth import check_user_type
from app.models.User import Client
from app.models.Client import Location, Utility, Assessment, Document
from app.models.Company import Company
from app.models.Chats import Chat
from app.models.Transaction import Transaction, CarbonPurchase, AssessmentTransaction
from app.client.forms import AddCompanyForm, EditCompanyForm, AddLocationForm, EditLocationForm, AddUtilityForm, EditUtilityForm, AddAssessmentForm, EditAssessmentForm, AddDocumentForm, AddAssessmentTransactionForm
from app.client.accountforms import UpdatePersonalForm, ChangePasswordForm, UpdateCompanyForm, UpdatePaymentForm
from flask_socketio import emit, send, join_room, leave_room
from datetime import datetime
from string import ascii_lowercase
import random
import os
import threading



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
        if request.endpoint == 'client.companies':
            return
        if request.endpoint == 'client.company_add':
            return
        if request.endpoint == 'client.company_edit':
            return
        if request.endpoint == 'client.company_delete':
            return
        return redirect(url_for('staff.companies'))
        
    company = Company.query.get(session['company'])
    g.company = company



@client.route('/')
@login_required
@check_user_type(['admin', 'manager', 'consultant', 'client'])
def dashboard():
    overview = {
        'timerange': 0,
        'carbonfootprint': 0,
        'energyusage': 0,
        'waterusage': 0,
        'totalcarbonfootprint': 0,
        'carbonfootprintoffsetted': 0
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
            utilities['carbonfootprint'].append(float(utility.carbonfootprint))
            utilities['energyusage'].append(float(utility.energyusage))
            utilities['waterusage'].append(float(utility.waterusage))
            
            overview['totalcarbonfootprint'] += float(utility.carbonfootprint)
        
        latestUtilityData = utilitiesData.order_by(Utility.date.desc()).first()
        if latestUtilityData:
            timerange = int(datetime(latestUtilityData.date.year, latestUtilityData.date.month, 1).timestamp()) * 1000
            if timerange > overview['timerange']:
                overview['timerange'] = timerange
                overview['carbonfootprint'] = 0
                overview['energyusage'] = 0
                overview['waterusage'] = 0
            if timerange == overview['timerange']:
                overview['carbonfootprint'] += float(latestUtilityData.carbonfootprint)
                overview['energyusage'] += float(latestUtilityData.energyusage)
                overview['waterusage'] += float(latestUtilityData.waterusage)
            
        locations[location.id] = {
            'name': location.name,
            'timerange': utilities["timerange"],
            'carbonfootprint': utilities['carbonfootprint'],
            'energyusage': utilities['energyusage'],
            'waterusage': utilities['waterusage']
        }

    if g.company.plan == 'free':
        return render_template('client/dashboard_free.html', overview=overview, locations=locations)
    
    
    
    carbonpurchasesData = db.session.query(CarbonPurchase).filter_by(company=g.company.id)
    for carbonpurchase in carbonpurchasesData:
        overview['carbonfootprintoffsetted'] += carbonpurchase.offset
    
    overview['carbonfootprintexceeded'] = overview['totalcarbonfootprint'] - overview['carbonfootprintoffsetted']
    overview['locations'] = len(locations)
    
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
            'phone_number': company.phone_number,
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
            email = request.form.get("email")
            phone_number = request.form.get("phone_number")
            address = request.form.get("address")
            plan = request.form.get("plan")
            
            logo = "icon.jpg"

            company = Company(name=name, industry=industry, email=email, phone_number=phone_number, address=address, logo=logo, plan=plan)
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
    companyData = Company.query.get(company)
    
    form = EditCompanyForm()
    form.name.data = companyData.name
    form.industry.data = companyData.industry
    form.address.data = companyData.address
    form.email.data = companyData.email
    form.phone_number.data = companyData.phone_number
    form.plan.data = companyData.plan

    if form.validate_on_submit():
        try:
            name = request.form.get("name")
            industry = request.form.get("industry")
            email = request.form.get("email")
            phone_number = request.form.get("phone_number")
            address = request.form.get("address")
            plan = request.form.get("plan")

            if name:
                companyData.name = name
            if industry:
                companyData.industry = industry
            if email:
                companyData.email = email
            if phone_number:
                companyData.phone_number = phone_number
            if address:
                companyData.address = address
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
@check_user_type(['admin', 'manager', 'consultant', 'client'])
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
@check_user_type(['admin', 'manager', 'consultant', 'client'])
def location_add():
    form = AddLocationForm()

    if form.validate_on_submit():
        try:
            name = request.form.get("name")
            address = request.form.get("address")

            location = Location(company=g.company.id, name=name, address=address)
            db.session.add(location)
            db.session.commit()

            return redirect(url_for('client.locations'))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

    return render_template("client/location_add.html", form=form)



@client.route("/location/<location>/edit", methods=['GET', 'POST'])
@login_required
@check_user_type(['admin', 'manager', 'consultant', 'client'])
def location_edit(location):
    locationData = Location.query.get(location)
    
    form = EditLocationForm()
    form.name.data = locationData.name
    form.address.data = locationData.address

    if form.validate_on_submit():
        try:
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
@check_user_type(['admin', 'manager', 'consultant', 'client'])
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
@check_user_type(['admin', 'manager', 'consultant', 'client'])
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
@check_user_type(['admin', 'manager', 'consultant', 'client'])
def location_utility_add(location):
    form = AddUtilityForm()

    if form.validate_on_submit():
        try:
            name = request.form.get("name")
            date = datetime.strptime(
                request.form.get("date"), "%Y-%m-%d").date()
            energyusage = request.form.get("energyusage")
            waterusage = request.form.get("waterusage")
            
            energycarbonfootprint = float(energyusage) * 0.5 / 1000
            watercarbonfootprint = float(waterusage) * 0.2 / 1000
            carbonfootprint = round(energycarbonfootprint + watercarbonfootprint, 5)

            utility = Utility(company=g.company.id, location=location, name=name, date=date,
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
@check_user_type(['admin', 'manager', 'consultant', 'client'])
def location_utility_edit(location, utility):
    utilityData = Utility.query.get(utility)
    
    form = EditUtilityForm()
    form.name.data = utilityData.name
    form.date.data = utilityData.date
    form.energyusage.data = utilityData.energyusage
    form.waterusage.data = utilityData.waterusage

    if form.validate_on_submit():
        try:
            name = request.form.get("name")
            date = request.form.get("date")
            energyusage = request.form.get("energyusage")
            waterusage = request.form.get("waterusage")

            if name:
                utilityData.name = name
            if date:
                utilityData.date = datetime.strptime(date, "%Y-%m-%d").date()
            if energyusage:
                utilityData.energyusage = energyusage
            if waterusage:
                utilityData.waterusage = waterusage
            
            energycarbonfootprint = float(utilityData.energyusage) * 0.5 / 1000
            watercarbonfootprint = float(utilityData.waterusage) * 0.2 / 1000
            carbonfootprint = round(energycarbonfootprint + watercarbonfootprint, 5)
            
            utilityData.carbonfootprint = carbonfootprint

            db.session.commit()

            return redirect(url_for('client.location_utility', location=location))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

    return render_template("client/utility_edit.html", form=form)



@client.route("/location/<location>/utility/delete/<utility>")
@login_required
@check_user_type(['admin', 'manager', 'consultant', 'client'])
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
@check_user_type(['admin', 'manager', 'consultant', 'client'])
def assessments():
    assessments = {}
    assessmentsData = db.session.query(Assessment).filter_by(company=g.company.id)
    for assessment in assessmentsData:
        assessments[assessment.id] = {
            'location': assessment.location,
            'name': assessment.name,
            'type': assessment.type,
            'progress': assessment.progress,
        }

    return render_template('client/assessments.html', assessments=assessments)



@client.route("/assessment/<assessment>")
@login_required
@check_user_type(['admin', 'manager', 'consultant', 'client'])
def assessment(assessment):
    assessmentData = db.session.query(Assessment).filter_by(company=g.company.id,id=assessment).first()
    
    documents = {}
    for documentID in assessmentData.documents:
        document = db.session.query(Document).filter_by(company=g.company.id, assessment=assessment, id=documentID).first()
        documents[documentID] = document

    return render_template('client/assessment.html', assessment=assessmentData, documents=documents)



@client.route("/assessment/add", methods=['GET', 'POST'])
@login_required
@check_user_type(['admin', 'manager', 'consultant'])
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
@check_user_type(['admin', 'manager', 'consultant'])
def assessment_edit(assessment):
    assessmentData = Assessment.query.get(assessment)
    
    form = EditAssessmentForm()
    form.location.data = assessmentData.location
    form.name.data = assessmentData.name
    form.type.data = assessmentData.type
    form.progress.data = assessmentData.progress

    if form.validate_on_submit():
        try:
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
@check_user_type(['admin', 'manager', 'consultant'])
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



@client.route("/assessment/<assessment>/transaction/add", methods=['GET', 'POST'])
@login_required
@check_user_type(['admin', 'manager'])
def assessment_transaction_add(assessment):
    form = AddAssessmentTransactionForm()

    if form.validate_on_submit():
        try:
            company = g.company.id
            name = request.form.get("name")
            description = request.form.get("description")
            date = datetime.strptime(request.form.get("date"), "%Y-%m-%d").date()
            price = request.form.get("price")

            transaction = Transaction(company=company, name=name, date=date, price=price)
            db.session.add(transaction)
            
            assessmentTransaction = AssessmentTransaction(company=company, assessment=assessment, name=name, description=description, date=date, price=price)
            db.session.add(assessmentTransaction)
            
            db.session.commit()
            
            thread = threading.Thread(target=email_transaction, args=(g.company.email, current_user.username, price, f"Assessment Transaction - {name}"))
            thread.start()

            return redirect(url_for('client.assessments'))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()
    else:
        flash("Payment Method Validation Error!")
        for input in form:
            if input.errors:
                flash(f'\n{input.name} - {input.errors[0]}')

    return render_template("client/assessment_transaction_add.html", form=form)






@client.route("/assessment/<assessment>/document/<document>", methods=['GET', 'POST'])
@login_required
@check_user_type(['admin', 'manager', 'consultant', 'client'])
def document(assessment, document):
    document = db.session.query(Document).filter_by(company=g.company.id, assessment=assessment, id=document).first()
    
    if request.method == 'POST' and current_user.type != 'client':
        try:
            content = request.form.get("docContent")
            document.content = content

            db.session.commit()
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

    return render_template('client/document.html', assessment=assessment, document=document)



@client.route("/assessment/<assessment>/document/<document>/download")
@login_required
@check_user_type(['admin', 'manager', 'consultant', 'client'])
def document_download(assessment, document):
    document = db.session.query(Document).filter_by(company=g.company.id, assessment=assessment, id=document).first()

    return render_template('client/document_download.html', assessment=assessment, document=document)



@client.route("/assessment/<assessment>/document/add", methods=['GET', 'POST'])
@login_required
@check_user_type(['admin', 'manager', 'consultant'])
def document_add(assessment):
    form = AddDocumentForm()

    if form.validate_on_submit():
        try:
            name = request.form.get("name")
            timestamp = datetime.now()

            document = Document(company=g.company.id, assessment=assessment, name=name, created=timestamp, updated=timestamp, content="")
            db.session.add(document)
            
            assessmentData = db.session.query(Assessment).filter_by(company=g.company.id,id=assessment).first()
            assessmentData.documents.append(document.id)
            flag_modified(assessmentData, 'documents')
            
            db.session.commit()
            return redirect(url_for('client.document', assessment=assessment, document=document.id))
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

    return render_template("client/document_add.html", form=form)



@client.route("/assessment/<assessment>/document/<document>/delete")
@login_required
@check_user_type(['admin', 'manager', 'consultant'])
def document_delete(assessment, document):
    try:
        document = db.session.query(Document).filter_by(company=g.company.id, assessment=assessment, id=document).first()
        
        assessmentData = db.session.query(Assessment).filter_by(company=g.company.id,id=assessment).first()
        assessmentData.documents.remove(document.id)
        flag_modified(assessmentData, 'documents')
        
        db.session.delete(document)
        db.session.commit()
    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()

    return redirect(url_for('client.assessment', assessment=assessment))






@client.route("/account")
@login_required
def account():
    if current_user.type != 'client':
        return redirect(url_for('auth.account'))
    
    form1 = UpdatePersonalForm()
    form1.first_name.data = current_user.first_name
    form1.last_name.data = current_user.last_name
    form1.username.data = current_user.username
    form1.email.data = current_user.email
    form1.phone_number.data = current_user.phone_number
    form1.profile_picture.data = current_user.profile_picture
    
    form2 = ChangePasswordForm()
    
    form3 = UpdateCompanyForm()
    form3.email.data = g.company.email
    form3.phone_number.data = g.company.phone_number
    form3.address.data = g.company.address
    form3.logo.data = g.company.logo
    
    transactions = {}
    transactionsData = db.session.query(Transaction).filter_by(company=g.company.id)
    for transaction in transactionsData:
        transactions[transaction.id] = {
            'name': transaction.name,
            'date': transaction.date,
            'price': transaction.price,
        }
    
    return render_template("client/account.html", form1=form1, form2=form2, form3=form3, transactions=transactions)



@client.route("/account/update/personal", methods=["POST"])
@login_required
@check_user_type(['client'])
def account_update_personal():
    form = UpdatePersonalForm()
    
    if form.validate_on_submit():
        try:
            userData = Client.query.get(current_user.id)
            
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

    return redirect(url_for('client.account'))



@client.route("/account/update/password", methods=["POST"])
@login_required
@check_user_type(['client'])
def account_update_password():
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        try:
            userData = Client.query.get(current_user.id)
            
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

    return redirect(url_for('client.account'))



@client.route("/account/update/company", methods=["POST"])
@login_required
@check_user_type(['client'])
def account_update_company():
    form = UpdateCompanyForm()
    
    if form.validate_on_submit():
        try:
            companyData = Company.query.get(g.company.id)

            email = request.form.get("email")
            phone_number = request.form.get("phone_number")
            address = request.form.get("address")
            
            logo = form.logo.data
            logo_filename = "uploads/logo-"
            for i in range(10):
                logo_filename += random.choice(ascii_lowercase)
            logo.save(os.path.join(
                './app/static/images', f'{logo_filename}'
            ))

            companyData.email = email
            companyData.phone_number = phone_number
            companyData.address = address
            companyData.logo = logo_filename

            db.session.commit()
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()
    else:
        flash("Company Profile Validation Error!")
        for input in form:
            if input.errors:
                flash(f'\n{input.name} - {input.errors[0]}')

    return redirect(url_for('client.account', page='company-profile'))



@client.route("/account/update/payment", methods=["GET", "POST"])
@login_required
@check_user_type(['client'])
def account_update_payment():
    form = UpdatePaymentForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                companyData = Company.query.get(g.company.id)

                name = request.form.get("name")
                card_no = request.form.get("card_no")
                expiry_month = request.form.get("expiry-month")
                expiry_year = request.form.get("expiry-year")
                cvc = request.form.get("cvc")
                
                expiry = f"{expiry_month}/{expiry_year[2:]}"

                companyData.payment_name = name
                companyData.payment_card_no = card_no
                companyData.payment_expiry = expiry
                companyData.payment_cvc = cvc

                db.session.commit()
                
                return redirect(url_for('client.account', page='billing'))
            except Exception as e:
                print(f"Error occurred: {e}")
                db.session.rollback()
        else:
            flash("Payment Method Validation Error!")
            for input in form:
                if input.errors:
                    flash(f'\n{input.name} - {input.errors[0]}')

    return render_template("client/account_payment.html", form=form)



@client.route("/account/upgrade", methods=["GET", "POST"])
@login_required
@check_user_type(['client'])
def account_upgrade():
    form = UpdatePaymentForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                companyData = Company.query.get(g.company.id)

                name = request.form.get("name")
                card_no = request.form.get("card_no")
                expiry_month = request.form.get("expiry-month")
                expiry_year = request.form.get("expiry-year")
                cvc = request.form.get("cvc")
                
                expiry = f"{expiry_month}/{expiry_year[2:]}"

                companyData.payment_name = name
                companyData.payment_card_no = card_no
                companyData.payment_expiry = expiry
                companyData.payment_cvc = cvc
                
                companyData.plan = 'custom'
                
                
                
                company = g.company.id
                date = datetime.now()
                price = 50
    
                transaction = Transaction(company=company, name=f"Account Upgrade", date=date, price=price)
                db.session.add(transaction)
                
                db.session.commit()
                
                
                
                thread = threading.Thread(target=email_upgrade_account, args=(g.company.email, g.company.name, price, f"Account Upgrade"))
                thread.start()
                
                return redirect(url_for('client.account', page='billing'))
            except Exception as e:
                print(f"Error occurred: {e}")
                db.session.rollback()
        else:
            flash("Payment Method Validation Error!")
            for input in form:
                if input.errors:
                    flash(f'\n{input.name} - {input.errors[0]}')

    return render_template("client/account_upgrade.html", form=form)






@client.route('/chat')
def chats_client():
    company = g.company.id
    
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
            'timestamp': time.strftime("%d/%m/%Y %H:%M:%S"),
            'message': message['message']
        }
        messages.append(msg)
    
    return render_template('client/chat.html', room=chatData.id, messages=messages)



@socketio.on('message')
def onMessage(messageData, room):
    print('Room', room, 'Message', messageData)
    
    chatData = db.session.query(Chat).filter_by(id=room).first()
    chatData.messages.append(messageData)
    flag_modified(chatData, 'messages')
    db.session.commit()
    
    send(message=messageData, to=room)



@socketio.on('join')
def on_join(room):
    print('RoomJoin', room)
    join_room(room)