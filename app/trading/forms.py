from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired



class AddProjectForm(FlaskForm):
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Project's name"})
    options = [{'Convservation', 'Renewable', 'Methane'}]
    type = SelectField('Type of project', choices=options)
    submit = SubmitField("Add Location")

class EditProjectForm(FlaskForm):
    name = StringField(render_kw={"placeholder": "Name"})
    options = [{'Convservation', 'Renewable', 'Methane'}]
    type = SelectField('Type of project', choices=options)
    submit = SubmitField('Update Location')