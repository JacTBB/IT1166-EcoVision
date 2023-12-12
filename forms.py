from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField


class LoginForm(FlaskForm):
    username = StringField('Username', render_kw={"placeholder": "Username"})
    password = PasswordField('Password', render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')
