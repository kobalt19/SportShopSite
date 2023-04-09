from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired


class GoodsForm(FlaskForm):
    name = StringField('Название', validators={DataRequired()})
    price = IntegerField('Цена (руб.)', validators={DataRequired()})
    submit = SubmitField('Подтвердить')
