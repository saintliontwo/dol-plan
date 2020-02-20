from flask_wtf import FlaskForm
from wtforms import Form, SubmitField, StringField, validators
from wtforms.fields.html5 import DateField, IntegerField


class MyForm(FlaskForm):
    main_event = StringField('Центральное мероприятие:', [validators.Length(min=4, max=32, message="Укажите название центрального мероприятия"),
                                                          validators.DataRequired()])
    period = IntegerField('Номер смены:', [validators.NumberRange(min=1, max=4, message="Введите номер смены с 1 по 4"),
                                           validators.DataRequired()])
    date = DateField('Дата начала смены:', [validators.DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Подтвердить')