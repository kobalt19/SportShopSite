from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField
from wtforms.validators import DataRequired


class OrderForm(FlaskForm):
    date = DateField('Срок заказа', validators={DataRequired()})
    submit = SubmitField('Заказать')
