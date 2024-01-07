from flask import render_template, request
from app.client import client
from app.database import db
from flask_login import login_required



@client.route('/')
@login_required
def dashboard():
    overview = {
        'carbonfootprint': 100,
        'energyusage': 100,
        'waterusage': 100
    }
    
    locations = {
        '1': {
            'name': 'Building 1',
            'timerange': [50,60,70,80,90,100,110,120,130,140,150],
            'carbonfootprint': [7,8,8,9,9,9,10,11,14,14,15],
            'energyusage': [1,2,3,4,5,6,7,8,9,10,11],
            'waterusage': [5,4,3,2,6,5,7,4,2,3,4]
        },
        '2': {
            'name': 'Building 2',
            'timerange': [50,60,70,80,90,100,110,120,130,140,150],
            'carbonfootprint': [7,8,8,9,9,9,10,11,14,14,15],
            'energyusage': [1,2,3,4,5,6,7,8,9,10,11],
            'waterusage': [5,4,3,2,6,5,7,4,2,3,4]
        }
    }
    return render_template('client/dashboard_free.html', overview=overview, locations=locations)

@client.route("/locations")
@login_required
def locations():
    return "Manage All Locations"

@client.route("/location/<location>/utility")
@login_required
def location_utility_manage(location):
    return "Manage Utility Bills: " + location

@client.route("/account")
@login_required
def account():
    return render_template("client/account.html")