from flask import Flask, render_template
from flask_login import LoginManager
from app.config import Config
from app.database import db, query_data
from app.models.User import Client, Author, Technician, Consultant, Manager, Admin
from app.models.News import *
from app.models.Client import *
from app.models.Company import *
from app.models.Trading import *
from app.models.Contact import *
from app.models.Inventory import *
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO


socketio = SocketIO()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    with app.app_context():
        db.init_app(app)
        db.create_all()

        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)

        socketio.init_app(app, async_mode='threading')

        bcrypt = Bcrypt(app)

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
    
    
    
    @app.errorhandler(403)
    def forbidden(e):
        return render_template("403.html"), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    return app
