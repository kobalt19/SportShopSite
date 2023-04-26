from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import IntegerField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class GoodsForm(FlaskForm):
    name = StringField('Название', validators={DataRequired()})
    category = SelectField('Категория', validate_choice=False)
    description = TextAreaField('Описание товара', validators={DataRequired()})
    price = IntegerField('Цена (руб.)', validators={DataRequired()})
    image = FileField('Фото товара', validators={FileRequired(), FileAllowed({'img', 'jpg'}, 'Image only!')})
    submit = SubmitField('Подтвердить')
