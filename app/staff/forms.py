from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import InputRequired



class AddProductForm(FlaskForm):
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Name"})
    quantity = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Quantity"})
    submit = SubmitField("Add Product")

class EditProductForm(FlaskForm):
    name = StringField(render_kw={"placeholder": "Name"})
    quantity = IntegerField(render_kw={"placeholder": "Quantity"})
    submit = SubmitField('Update Product')