from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, EmailField
from wtforms.validators import DataRequired


class ArticleForm(FlaskForm):
    image_view_onNews = StringField(
        'Image', validators=[DataRequired()], render_kw={"placeholder": "Image"})
    title = StringField('Title', validators=[DataRequired()], render_kw={
                        "placeholder": "Title"})
    content = TextAreaField('Content', validators=[DataRequired()], render_kw={
                            "placeholder": "Content"})
    submit = SubmitField('Submit')


class ContactForm(FlaskForm):
    employee_name = StringField('Employee Name', validators=[
                                DataRequired()], render_kw={"placeholder": "Employee Name"})
    company_name = StringField('Company Name', validators=[
                               DataRequired()], render_kw={"placeholder": "Company Name"})
    company_email = EmailField('Company Email', validators=[
        DataRequired()], render_kw={"placeholder": "Company Email"})
    industry = StringField('Industry', validators=[DataRequired()], render_kw={
                           "placeholder": "Industry"})
    company_size = IntegerField('Company Size', validators=[
                                DataRequired()], render_kw={"placeholder": "Company Size"})
    submit = SubmitField("Submit")
