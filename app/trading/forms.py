from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired



class AddProjectForm(FlaskForm):
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Project's name"})
    stock = StringField(validators=[InputRequired()], render_kw={"placeholder": "Stock Level"})
    options = [('Convservation'), ('Renewable'), ('Methane')]
    type = SelectField('Type of project', choices=options)
    submit = SubmitField("Add Location")

class EditProjectForm(FlaskForm):
    name = StringField(render_kw={"placeholder": "Name"})
    stock = StringField(render_kw={"placeholder": "Stock level"})
    options = [('Convservation'), ('Renewable'), ('Methane')]
    type = SelectField('Type of project', choices=options)
    submit = SubmitField('Update Location')