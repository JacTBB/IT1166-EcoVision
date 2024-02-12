from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, IntegerField, FloatField
from wtforms.validators import InputRequired



class AddCompanyForm(FlaskForm):
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Name"})
    industry = StringField(validators=[InputRequired()], render_kw={"placeholder": "Industry"})
    email = StringField(validators=[InputRequired()], render_kw={"placeholder": "Email"})
    phone_number = StringField(validators=[InputRequired()], render_kw={"placeholder": "Phone Number"})
    address = StringField(validators=[InputRequired()], render_kw={"placeholder": "Address"})
    plan = SelectField(validators=[InputRequired()], choices=['free', 'custom'])

class EditCompanyForm(FlaskForm):
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Name"})
    industry = StringField(validators=[InputRequired()], render_kw={"placeholder": "Industry"})
    email = StringField(validators=[InputRequired()], render_kw={"placeholder": "Email"})
    phone_number = StringField(validators=[InputRequired()], render_kw={"placeholder": "Phone Number"})
    address = StringField(validators=[InputRequired()], render_kw={"placeholder": "Address"})
    plan = SelectField(validators=[InputRequired()], choices=['free', 'custom'])
    
    
    
class AddLocationForm(FlaskForm):
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Name"})
    address = StringField(validators=[InputRequired()], render_kw={"placeholder": "Address"})

class EditLocationForm(FlaskForm):
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Name"})
    address = StringField(validators=[InputRequired()], render_kw={"placeholder": "Address"})



class AddUtilityForm(FlaskForm):
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Name"})
    date = DateField(validators=[InputRequired()], render_kw={"placeholder": "Date"})
    energyusage = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Energy Usage"})
    waterusage = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Water Usage"})

class EditUtilityForm(FlaskForm):
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Name"})
    date = DateField(validators=[InputRequired()], render_kw={"placeholder": "Date"})
    energyusage = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Energy Usage"})
    waterusage = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Water Usage"})
    


class AddAssessmentForm(FlaskForm):
    location = StringField(validators=[InputRequired()], render_kw={"placeholder": "Location"})
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Name"})
    type = StringField(validators=[InputRequired()], render_kw={"placeholder": "Type"})
    progress = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Progress"})

class EditAssessmentForm(FlaskForm):
    location = StringField(validators=[InputRequired()], render_kw={"placeholder": "Location"})
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Name"})
    type = StringField(validators=[InputRequired()], render_kw={"placeholder": "Type"})
    progress = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Progress"})



class AddAssessmentTransactionForm(FlaskForm):
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Name"})
    description = StringField(validators=[InputRequired()], render_kw={"placeholder": "Description"})
    date = DateField(validators=[InputRequired()], render_kw={"placeholder": "Date"})
    price = FloatField(validators=[InputRequired()], render_kw={"placeholder": "Price"})
    


class AddDocumentForm(FlaskForm):
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Name"})