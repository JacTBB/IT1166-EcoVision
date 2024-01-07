from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired



class AddLocationForm(FlaskForm):
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Name"})
    address = StringField(validators=[InputRequired()], render_kw={"placeholder": "Address"})
    submit = SubmitField("Add Location")

class EditLocationForm(FlaskForm):
    name = StringField(render_kw={"placeholder": "Name"})
    address = StringField(render_kw={"placeholder": "Address"})
    submit = SubmitField('Update Location')