from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, DataRequired


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()], render_kw={
                           "placeholder": "Username"})
    password = PasswordField(validators=[DataRequired()], render_kw={
                             "placeholder": "Password"})
    submit = SubmitField('Login')
