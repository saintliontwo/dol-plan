from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, validators
from wtforms.fields.html5 import DateField, IntegerField


class MyForm(FlaskForm):
    main_event = StringField('Центральное мероприятие:', [validators.DataRequired()])
    period = IntegerField('Номер смены:', [validators.DataRequired()])
    date = DateField('Дата начала смены:', [validators.DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Подтвердить')
