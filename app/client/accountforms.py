from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, URLField, PasswordField
from wtforms.validators import DataRequired



class UpdatePersonalForm(FlaskForm):
    first_name = StringField(validators=[DataRequired()])
    last_name = StringField(validators=[DataRequired()])
    username = StringField(validators=[DataRequired()])
    email = EmailField(validators=[DataRequired()])
    phone_number = IntegerField(validators=[DataRequired()])
    profile_picture = URLField(validators=[DataRequired()])

class ChangePasswordForm(FlaskForm):
    password = PasswordField(validators=[DataRequired()], render_kw={"placeholder": "New Password"})



class UpdateCompanyForm(FlaskForm):
    email = EmailField(validators=[DataRequired()])
    phone_number = IntegerField(validators=[DataRequired()])
    address = StringField(validators=[DataRequired()])
    logo = URLField(validators=[DataRequired()])