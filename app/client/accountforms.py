from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, EmailField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length



def is_integer(form, field):
    try:
        int(field.data)
    except ValueError:
        raise ValidationError('Field must be an integer.')



class UpdatePersonalForm(FlaskForm):
    first_name = StringField(validators=[DataRequired()])
    last_name = StringField(validators=[DataRequired()])
    username = StringField(validators=[DataRequired()])
    email = EmailField(validators=[DataRequired()])
    phone_number = IntegerField(validators=[DataRequired()])
    profile_picture = FileField(validators=[FileAllowed(['png','jpg','jpeg'], 'Images Only!')])

class ChangePasswordForm(FlaskForm):
    password = PasswordField(validators=[DataRequired()], render_kw={"placeholder": "New Password"})



class UpdateCompanyForm(FlaskForm):
    email = EmailField(validators=[DataRequired()])
    phone_number = IntegerField(validators=[DataRequired()])
    address = StringField(validators=[DataRequired()])
    logo = FileField(validators=[FileAllowed(['png','jpg','jpeg'], 'Images Only!')])



class UpdatePaymentForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    card_no = StringField(validators=[DataRequired(), Length(min=16,max=16), is_integer])
    cvc = StringField(validators=[DataRequired(), Length(min=3,max=4), is_integer])