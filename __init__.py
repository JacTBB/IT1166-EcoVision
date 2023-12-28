from concurrent.futures import thread
from enum import auto
import os
from flask import Flask, render_template, request, send_from_directory

# local python files
from create_database import *
from forms import *
from models import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "1234567890"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db.init_app(app)
STATIC_URL = 'static/'

with app.app_context():
    db.create_all()  # create database tables for our data models


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    news = shelve.open("news")
    get_maxPosts = max(news.keys())
    display_posts = str(int(get_maxPosts) - 2)

    return render_template('index.html', title='Home', selected="home", news=sorted(news.items(), reverse=True), maxPosts=get_maxPosts, display_posts=display_posts)


@app.route('/services')
def services():

    return render_template('services.html', title='Services', selected="services")


@app.route('/news')
def news():
    news = shelve.open("news").items()
    postid = request.args.get('postid')
    if postid is not None:
        news = shelve.open("news")
        return render_template('article.html',
                               title=news[str(postid)].title +
                               " | News Article",
                               selected='article',
                               article=news[str(postid)])
    return render_template('news.html', title='News', selected="news", data=sorted(news, reverse=True))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        result = request.form
        username = result.get("username")
        password = result.get("password")
        return render_template("account.html", username=username, password=password)

    return render_template("login.html", form=form, title='Login', selected="login")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('oops.html'), 404


if __name__ in '__main__':
    with app.app_context():
        # Query user = User.query.filter_by(name='John Doe').first()

        User = User.query.all()
        Author = Author.query.all()
        Admin = Admin.query.all()

        print(User)
        print(Author)
        print(Admin)

    app.run(debug=True)
