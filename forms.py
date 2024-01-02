from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_ckeditor import CKEditorField, CKEditor
from wtforms.validators import InputRequired, DataRequired



class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()], render_kw={
                           "placeholder": "Username"})
    password = PasswordField(validators=[InputRequired()], render_kw={
                             "placeholder": "Password"})
    submit = SubmitField("Login")


class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = CKEditorField('Content')
    submit = sumbit = SubmitField('Submit')
