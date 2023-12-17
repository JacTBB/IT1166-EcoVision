import os
from flask import Flask, render_template, request, url_for, send_from_directory

# local python files
from news import *
from forms import *


app = Flask(__name__)
app.config["SECRET_KEY"] = "1234567890"

STATIC_URL = 'static/'


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    news = shelve.open("news").items()
    return render_template('index.html', title='Home', selected="home", news=sorted(news, reverse=True))


@app.route('/services')
def services():

    return render_template('services.html', title='Services', selected="services")


@app.route('/news')
def news():
    news = shelve.open("news").items()

    return render_template('news.html', title='News', selected="news", data=sorted(news, reverse=True))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.is_submitted():
        result = request.form
        username = result.get("username")
        password = result.get("password")
        return render_template("account.html", username=username, password=password)

    return render_template("login.html", form=form, title='Login', selected="login")


if __name__ in '__main__':
    app.run(debug=True)
