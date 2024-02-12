from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField
from wtforms.validators import InputRequired



class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()], render_kw={"placeholder": "Username", 'autofocus': True})
    password = PasswordField(validators=[InputRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    first_name = StringField(validators=[InputRequired()], render_kw={"placeholder": "First Name", 'autofocus': True})
    last_name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Last Name"})
    username = StringField(validators=[InputRequired()], render_kw={"placeholder": "Username"})
    email = EmailField(validators=[InputRequired()], render_kw={"placeholder": "Email"})
    phone_number = StringField(validators=[InputRequired()], render_kw={"placeholder": "Phone Number"})
    password = PasswordField(validators=[InputRequired()], render_kw={"placeholder": "Password"})
    
    company_name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Company Name"})
    company_industry = StringField(validators=[InputRequired()], render_kw={"placeholder": "Company Industry"})
    company_email = EmailField(validators=[InputRequired()], render_kw={"placeholder": "Company Email"})
    company_phone_number = StringField(validators=[InputRequired()], render_kw={"placeholder": "Company Phone number"})
    company_address = StringField(validators=[InputRequired()], render_kw={"placeholder": "Company Address"})
    
    submit = SubmitField("Register")

class AddUserForm(FlaskForm):
    first_name = StringField(validators=[InputRequired()], render_kw={"placeholder": "First Name"})
    last_name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Last Name"})
    username = StringField(validators=[InputRequired()], render_kw={"placeholder": "Username"})
    email = EmailField(validators=[InputRequired()], render_kw={"placeholder": "Email"})
    phone_number = StringField(validators=[InputRequired()], render_kw={"placeholder": "Phone Number"})
    password = PasswordField(validators=[InputRequired()], render_kw={"placeholder": "Password"})

class EditUserForm(FlaskForm):
    first_name = StringField(render_kw={"placeholder": "First Name"})
    last_name = StringField(render_kw={"placeholder": "Last Name"})
    username = StringField(render_kw={"placeholder": "Username"})
    email = EmailField(render_kw={"placeholder": "Email"})
    phone_number = StringField(render_kw={"placeholder": "Phone Number"})