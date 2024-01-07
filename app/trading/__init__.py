from flask import Blueprint



trading = Blueprint('trading', __name__)



from app.trading import routes