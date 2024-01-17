from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import InputRequired
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired


class AddProjectForm(FlaskForm):
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Project's name"})
    stock = StringField(validators=[InputRequired()], render_kw={"placeholder": "Stock Amount"})
    options = [('Convservation'), ('Renewable'), ('Methane')]
    type = SelectField('Type of project', choices=options)
    price = StringField(validators=[InputRequired()], render_kw={"placeholder": "Stock Price"})
    submit = SubmitField("Add Project")

class EditProjectForm(FlaskForm):
    name = StringField(render_kw={"placeholder": "Name"})
    stock = StringField(render_kw={"placeholder": "Stock Amount"})
    options = [('Convservation'), ('Renewable'), ('Methane')]
    type = SelectField('Type of project', choices=options)
    price = StringField(validators=[InputRequired()], render_kw={"placeholder": "Stock Price"})
    submit = SubmitField('Update Project')

class ProjectDetailsForm(FlaskForm):
    content = CKEditorField('Content')
    submit = SubmitField('Submit')

class AddToCart(FlaskForm):
    stock = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Stock Amount"})
    submit = SubmitField("Add to Cart")