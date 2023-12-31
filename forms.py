from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, DataRequired
from flask_ckeditor import CKEditorField, CKEditor


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()], render_kw={
                           "placeholder": "Username"})
    password = PasswordField(validators=[InputRequired()], render_kw={
                             "placeholder": "Password"})
    submit = SubmitField("Login")


class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = CKEditorField('Content')
