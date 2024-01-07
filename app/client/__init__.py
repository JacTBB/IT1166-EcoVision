from flask import Blueprint



client = Blueprint('client', __name__)



from app.client import routes