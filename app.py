import os
from flask import Flask, render_template, request, send_from_directory

# local python files
# from create_database import *
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
    query = db.session.query(Post).order_by(Post.date.desc()).limit(3).all()

    for i, post in enumerate(query):
        print(f"Post {i+1}: {post.id}")

    return render_template('index.html', title='Home', selected="home", news=query)


@app.route('/services')
def services():

    return render_template('services.html', title='Services', selected="services")


@app.route('/news')
def news():
    query = db.session.query(Post).order_by(Post.date.desc()).all()
    postid = request.args.get('postid')
    print(query)
    # if postid is not None:
    #     news = shelve.open("news")
    #     return render_template('article.html',
    #                            title=news[str(postid)].title +
    #                            " | News Article",
    #                            selected='article',
    #                            article=news[str(postid)])
    return render_template('news.html', title='News', selected="news", data=query)
    return "Under Maintenance"


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        result = request.form

        try:
            username = result.get("username")

            query = db.session.query(Customer).filter_by(
                username=username).first()

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
