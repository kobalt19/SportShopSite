from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CategoryForm(FlaskForm):
    name = StringField('Название категории', validators={DataRequired()})
    submit = SubmitField('Подтвердить')
