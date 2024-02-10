from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, IntegerField
from wtforms.validators import InputRequired



class AddCompanyForm(FlaskForm):
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Name"})
    industry = StringField(validators=[InputRequired()], render_kw={"placeholder": "Industry"})
    address = StringField(validators=[InputRequired()], render_kw={"placeholder": "Address"})
    email = StringField(validators=[InputRequired()], render_kw={"placeholder": "Email"})
    plan = SelectField(validators=[InputRequired()], choices=['free', 'custom'])

class EditCompanyForm(FlaskForm):
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Name"})
    industry = StringField(validators=[InputRequired()], render_kw={"placeholder": "Industry"})
    address = StringField(validators=[InputRequired()], render_kw={"placeholder": "Address"})
    email = StringField(validators=[InputRequired()], render_kw={"placeholder": "Email"})
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
    carbonfootprint = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Carbon Footprint"})
    energyusage = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Energy Usage"})
    waterusage = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Water Usage"})

class EditUtilityForm(FlaskForm):
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Name"})
    date = DateField(validators=[InputRequired()], render_kw={"placeholder": "Date"})
    carbonfootprint = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Carbon Footprint"})
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
    


class AddDocumentForm(FlaskForm):
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Name"})