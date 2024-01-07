from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired



class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = CKEditorField('Content')
    submit = SubmitField('Submit')

class ContactForm(FlaskForm):
    text = StringField('Text', validators=[DataRequired()])
    submit = SubmitField("Submit")