from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import InputRequired
from wtforms.validators import DataRequired


class AddProjectForm(FlaskForm):
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Project's name"})
    stock = StringField(validators=[InputRequired()], render_kw={"placeholder": "Stock Amount"})
    options = [('Conservation'), ('Renewable'), ('Methane')]
    type = SelectField('Type of project', choices=options)
    price = StringField(validators=[InputRequired()], render_kw={"placeholder": "Stock Price"})
    submit = SubmitField("Add Project")

class EditProjectForm(FlaskForm):
    name = StringField(render_kw={"placeholder": "Name"})
    stock = StringField(render_kw={"placeholder": "Stock Amount"})
    options = [('Conservation'), ('Renewable'), ('Methane')]
    type = SelectField('Type of project', choices=options)
    price = StringField(validators=[InputRequired()], render_kw={"placeholder": "Stock Price"})
    submit = SubmitField('Update Project')

class ProjectDetailsForm(FlaskForm):
    content = StringField(validators=[InputRequired()])

class AddToCart(FlaskForm):
    stock = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Stock Amount"})