from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import InputRequired



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