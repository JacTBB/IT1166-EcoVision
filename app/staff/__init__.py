from flask import Blueprint



staff = Blueprint('staff', __name__)



from app.staff import routes