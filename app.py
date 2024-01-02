import os
from flask import Flask, make_response, redirect, render_template, request, send_from_directory, session, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user


# local python files
from forms import *
from models import *


app = Flask(__name__)
app.config["SECRET_KEY"] = "1234567890"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SESSION_COOKIE_SECURE"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = False
app.secret_key = "123"

login_manager = LoginManager()
login_manager.init_app(app)

STATIC_URL = 'static/'

ckeditor = CKEditor(app)
db.init_app(app)

with app.app_context():
    db.create_all()  # create database tables for our data models


def query_data(model, limit=None, order_by=None, filter_by=None, all=True):
    query = db.session.query(model)

    if order_by is not None:
        query = query.order_by(order_by)

    if limit is not None:
        query = query.limit(limit)

    if filter_by is not None:
        query = query.filter_by(**filter_by)

    if limit is not None and order_by is not None:
        query = query.order_by(order_by).limit(limit)

    if limit is not None and filter_by is not None:
        query = query.filter_by(**filter_by).limit(limit)

    if all is False:
        return query.first()

    return query.all()


def query_login(model, user, pw):
    query = query_data(model, filter_by={
        'username': user}, all=False)
    if query is not None:
        if query.username == user and query.check_password(pw):
            return True


@app.before_request
def check_login():
    return


@app.route("/admin")
def admin():
    return "hi"


@login_manager.user_loader
def user_loader(user_id):
    return query_data(Customer, filter_by={'id': user_id}, all=False)


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    customer = query_data(Customer, filter_by={
                          'username': username}, all=False)
    return customer


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    return render_template('index.html', title='Home', selected="home", news=query_data(Post, limit=3))


@app.route('/services')
def services():
    return render_template('services.html', title='Services', selected="services")


@app.route('/news')
def news():
    query = query_data(Post)
    postid = request.args.get('postid')
    if postid is not None:
        form = ArticleForm()
        query = query_data(Post, filter_by={'postid': postid}, all=False)
        if query is not None:
            return render_template('article.html',
                                   title=query.title,
                                   selected='article',
                                   article=query, form=form, userType=session.get('type'))

    return render_template('news.html', title='News', selected="news", data=query)
    return "Under Maintenance"


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error_message = None
    admin = request.args.get('admin')
    requestAdminLogin = False
    showLogout = None
    if admin is not None:
        requestAdminLogin = True

    if form.validate_on_submit():
        try:
            username = request.form.get("username")
            password = request.form.get("password")
            if admin is not None:
                if query_login(Admin, username, password):
                    return render_template("account.html", password=password, username=username)
                else:
                    error_message = "Invalid username or password"
            else:
                if query_login(Customer, username, password):
                    customer = query_data(Customer, filter_by={
                                          'username': username}, all=False)
                    login_user(customer)
                    return redirect(url_for('protected'))
                else:
                    error_message = "Invalid username or password"

            db.session.commit()
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

        if session.get("username") is not None:
            showLogout = True

    return render_template("login.html", form=form, title='Login', selected="login", showLogout=showLogout, error_message=error_message, requestAdminLogin=requestAdminLogin)


@app.route("/protected")
@login_required
def protected():
    if current_user.is_authenticated:
        username = current_user.username
    else:
        username = "Guest"
    return f"Logged in as: { username}"


@app.route('/logout')
def logout():
    logout_user()
    return "Logged out"


@app.errorhandler(404)
def page_not_found(e):
    return render_template('oops.html'), 404


if __name__ in '__main__':
    app.run(port=80, debug=True)
