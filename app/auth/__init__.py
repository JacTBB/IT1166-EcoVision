from flask import Blueprint, abort
from flask_login import current_user
from functools import wraps



auth = Blueprint('auth', __name__)



def check_user_type(userTypes):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.type in userTypes:
                return func(*args, **kwargs)
            abort(403)
        return wrapper
    return decorator



from app.auth import routes