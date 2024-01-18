from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, IntegerField
from wtforms.validators import InputRequired



class AddCompanyForm(FlaskForm):
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Name"})
    industry = StringField(validators=[InputRequired()], render_kw={"placeholder": "Industry"})
    address = StringField(validators=[InputRequired()], render_kw={"placeholder": "Address"})
    email = StringField(validators=[InputRequired()], render_kw={"placeholder": "Email"})
    plan = SelectField(validators=[InputRequired()], choices=['free', 'custom'])
    submit = SubmitField("Add Company")

class EditCompanyForm(FlaskForm):
    name = StringField(render_kw={"placeholder": "Name"})
    industry = StringField(render_kw={"placeholder": "Industry"})
    address = StringField(render_kw={"placeholder": "Address"})
    email = StringField(render_kw={"placeholder": "Email"})
    plan = SelectField(choices=['free', 'custom'])
    submit = SubmitField('Update Company')
    
    
    
class AddLocationForm(FlaskForm):
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Name"})
    address = StringField(validators=[InputRequired()], render_kw={"placeholder": "Address"})
    submit = SubmitField("Add Location")

class EditLocationForm(FlaskForm):
    name = StringField(render_kw={"placeholder": "Name"})
    address = StringField(render_kw={"placeholder": "Address"})
    submit = SubmitField('Update Location')



class AddUtilityForm(FlaskForm):
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Name"})
    date = DateField(validators=[InputRequired()], render_kw={"placeholder": "Date"})
    carbonfootprint = StringField(validators=[InputRequired()], render_kw={"placeholder": "Carbon Footprint"})
    energyusage = StringField(validators=[InputRequired()], render_kw={"placeholder": "Energy Usage"})
    waterusage = StringField(validators=[InputRequired()], render_kw={"placeholder": "Water Usage"})
    submit = SubmitField("Add Utility")

class EditUtilityForm(FlaskForm):
    name = StringField(render_kw={"placeholder": "Name"})
    date = DateField(render_kw={"placeholder": "Date"})
    carbonfootprint = StringField(render_kw={"placeholder": "Carbon Footprint"})
    energyusage = StringField(render_kw={"placeholder": "Energy Usage"})
    waterusage = StringField(render_kw={"placeholder": "Water Usage"})
    submit = SubmitField('Update Utility')
    


class AddAssessmentForm(FlaskForm):
    location = StringField(validators=[InputRequired()], render_kw={"placeholder": "Location"})
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Name"})
    type = StringField(validators=[InputRequired()], render_kw={"placeholder": "Type"})
    progress = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Progress"})
    submit = SubmitField("Add Assessment")

class EditAssessmentForm(FlaskForm):
    location = StringField(render_kw={"placeholder": "Location"})
    name = StringField(render_kw={"placeholder": "Name"})
    type = StringField(render_kw={"placeholder": "Type"})
    progress = IntegerField(render_kw={"placeholder": "Progress"})
    submit = SubmitField('Update Assessment')