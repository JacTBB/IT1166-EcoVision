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
    employee_name = StringField('Employee Name', validators=[DataRequired()])
    company_name = StringField('Company Name', validators=[DataRequired()])
    company_email = StringField('Company Email', validators=[DataRequired()])
    industry = StringField('Industry', validators=[DataRequired()])
    company_size = IntegerField('Company Size', validators=[DataRequired()])
    submit = SubmitField("Submit")

    # employee_name: Mapped[str] = mapped_column(String)
    # company_name: Mapped[str] = mapped_column(String)
    # company_email: Mapped[str] = mapped_column(String)
    # industry: Mapped[str] = mapped_column(String)
    # company_size: Mapped[int] = mapped_column(Integer)
