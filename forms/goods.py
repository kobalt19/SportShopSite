from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class GoodsForm(FlaskForm):
    name = StringField('Название', validators={DataRequired()})
    category = StringField('Категория', validators={DataRequired()})
    description = TextAreaField('Описание товара', validators={DataRequired()})
    price = IntegerField('Цена (руб.)', validators={DataRequired()})
    submit = SubmitField('Подтвердить')
