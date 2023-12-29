import os
from flask import Flask, render_template, request, send_from_directory
from sqlalchemy import column, false

# local python files
from forms import *
from models import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "1234567890"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db.init_app(app)
STATIC_URL = 'static/'

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
        query = query_data(Post, filter_by={'postid': postid}, all=False)
        if query is not None:
            return render_template('article.html',
                                   title=query.title +  # type: ignore
                                   " | News Article",
                                   selected='article',
                                   article=query)
    return render_template('news.html', title='News', selected="news", data=query)
    return "Under Maintenance"


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        result = request.form

        try:
            username = result.get("username")
            query = query_data(Customer, filter_by={
                               'username': username}, all=False)

            if query is not None:
                if query.username == result.get("username") and query.password == result.get("password"):
                    return render_template("account.html", username=query.username, password=query.password)

            db.session.commit()
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

    return render_template("login.html", form=form, title='Login', selected="login")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('oops.html'), 404


if __name__ in '__main__':
    app.run(port=80, debug=True)
