from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField, FloatField, SelectField
from wtforms.validators import InputRequired


class AddProductForm(FlaskForm):
    name = StringField(validators=[InputRequired()], render_kw={
                       "placeholder": "Name"})
    quantity = IntegerField(validators=[InputRequired()], render_kw={
                            "placeholder": "Quantity"})
    submit = SubmitField("Add Product")


class EditProductForm(FlaskForm):
    name = StringField(render_kw={"placeholder": "Name"})
    quantity = IntegerField(render_kw={"placeholder": "Quantity"})
    submit = SubmitField('Update Product')


class AddCompanyInfo(FlaskForm):
    employee_name = StringField(render_kw={"placeholder": "Employee Name"})
    company_name = StringField(render_kw={"placeholder": "Company Name"})
    company_email = StringField(render_kw={"placeholder": "Company Email"})
    industry = StringField(render_kw={"placeholder": "Industry"})
    company_size = StringField(render_kw={"placeholder": "Company Size"})
    submit = SubmitField('Add Company Info')


class EditCompanyInfo(FlaskForm):
    id = IntegerField(render_kw={"placeholder": "ID"})
    employee_name = StringField(render_kw={"placeholder": "Employee Name"})
    company_name = StringField(render_kw={"placeholder": "Company Name"})
    company_email = StringField(render_kw={"placeholder": "Company Email"})
    industry = StringField(render_kw={"placeholder": "Industry"})
    company_size = StringField(render_kw={"placeholder": "Company Size"})
    submit = SubmitField('Update Company Info')



class AddTaskForm(FlaskForm):
    user_id = SelectField(validators=[InputRequired()], choices=[])
    description = StringField(validators=[InputRequired()], render_kw={"placeholder": "Task Description"})



class AnnouncementForm(FlaskForm):
    description = StringField(validators=[InputRequired()], render_kw={"placeholder": "Description"})



class AddTransactionForm(FlaskForm):
    company = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Company"})
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Name"})
    date = DateField(validators=[InputRequired()], render_kw={"placeholder": "Date"})
    price = FloatField(validators=[InputRequired()], render_kw={"placeholder": "Price"})