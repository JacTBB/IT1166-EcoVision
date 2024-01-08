from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired


class ArticleForm(FlaskForm):
    image_view_onNews = StringField('Image', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    content = CKEditorField('Content')
    submit = SubmitField('Submit')


class ContactForm(FlaskForm):
    employee_name = StringField('employee_name', validators=[DataRequired()])
    company_name = StringField('company_name', validators=[DataRequired()])
    company_email = StringField('company_email', validators=[DataRequired()])
    industry = StringField('industry', validators=[DataRequired()])
    company_size = IntegerField('company_size', validators=[DataRequired()])
    submit = SubmitField("Submit")

    # employee_name: Mapped[str] = mapped_column(String)
    # company_name: Mapped[str] = mapped_column(String)
    # company_email: Mapped[str] = mapped_column(String)
    # industry: Mapped[str] = mapped_column(String)
    # company_size: Mapped[int] = mapped_column(Integer)
