from flask import Flask
from flask_login import LoginManager
from app.config import Config
from app.database import db, query_data
from app.models.User import Client, Author, Technician, Consultant, Manager, Admin
from app.models.News import *
from app.models.Client import *
from app.models.Trading import *
from flask_bcrypt import Bcrypt
from flask_ckeditor import CKEditor



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    with app.app_context():
        db.init_app(app)
        db.create_all()
    
        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)
        
        bcrypt = Bcrypt(app)
        
        ckeditor = CKEditor()
        ckeditor.init_app(app)
        
        
        
        @login_manager.user_loader
        def user_loader(user_id):
            return (query_data(Client, filter_by={'user_id': user_id}, all=False) or
                    query_data(Author, filter_by={'user_id': user_id}, all=False) or
                    query_data(Technician, filter_by={'user_id': user_id}, all=False) or
                    query_data(Consultant, filter_by={'user_id': user_id}, all=False) or
                    query_data(Manager, filter_by={'user_id': user_id}, all=False) or
                    query_data(Admin, filter_by={'user_id': user_id}, all=False))



        from app.main import main
        from app.auth import auth
        from app.client import client
        from app.trading import trading
        from app.staff import staff
        
        app.register_blueprint(main)
        app.register_blueprint(auth)
        app.register_blueprint(client, url_prefix='/client')
        app.register_blueprint(trading, url_prefix='/trading')
        app.register_blueprint(staff, url_prefix='/staff')

    return app