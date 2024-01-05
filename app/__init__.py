from flask import Flask
from flask_login import LoginManager
from app.config import Config
from app.database import db, query_data
from app.models.User import Customer
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
            return query_data(Customer, filter_by={'id': user_id}, all=False)

        @login_manager.request_loader
        def request_loader(request):
            username = request.form.get('username')
            customer = query_data(Customer, filter_by={'username': username}, all=False)
            return customer



        from app.main import main
        from app.auth import auth
        
        app.register_blueprint(main)
        app.register_blueprint(auth)

    return app