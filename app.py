from flask import Flask, render_template, request
from wtforms import *
from forms import *


app = Flask(__name__)
app.config["SECRET_KEY"] = "1234567890"
app.config["WTF_CSRF_ENABLED"] = False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.is_submitted():
        result = request.form
        username = result.get("username")
        password = result.get("password")
        return render_template("account.html", username=username, password=password)

    return render_template("login.html", form=form)


if __name__ in '__main__':
    app.run()
