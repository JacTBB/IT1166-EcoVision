from flask import render_template, request, redirect, url_for
from app.client import client
from app.database import db
from flask_login import login_required
from app.models.Client import Location, Utility
from app.client.forms import AddLocationForm, EditLocationForm, AddUtilityForm, EditUtilityForm
from datetime import datetime


@client.route('/')
@login_required
def dashboard():
    overview = {
        'carbonfootprint': 100,
        'energyusage': 100,
        'waterusage': 100
    }

    locations = {}
    locationsData = db.session.query(Location).all()
    for location in locationsData:
        locations[location.id] = {
            'name': location.name,
            'timerange': [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150],
            'carbonfootprint': [7, 8, 8, 9, 9, 9, 10, 11, 14, 14, 15],
            'energyusage': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            'waterusage': [5, 4, 3, 2, 6, 5, 7, 4, 2, 3, 4]
        }

    return render_template('client/dashboard_free.html', overview=overview, locations=locations)


@client.route("/locations")
@login_required
def locations():
    locations = {}
    locationsData = db.session.query(Location).all()
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
    utilitiesData = db.session.query(Utility).all()
    for utility in utilitiesData:
        utilities[utility.id] = {
            'location': utility.location,
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


@client.route("/account")
@login_required
def account():
    return render_template("auth/account.html")
