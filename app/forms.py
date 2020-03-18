from flask_wtf import FlaskForm
from wtforms import Form, SubmitField, StringField, validators
from wtforms.fields.html5 import DateField, IntegerField


class MyForm(FlaskForm):
    main_event = StringField('Центральное мероприятие:', [validators.Length(min=4, max=32, ),
                                                          validators.DataRequired(message="Название центрального "
                                                                                          "мероприятия должно быть "
                                                                                          "длинее 4 символов")])
    period = IntegerField('Номер смены:', [validators.NumberRange(min=1, max=4, ),
                                           validators.DataRequired(message="Введите номер смены с 1 по 4")])
    date = DateField('Дата начала смены:', [validators.DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Подтвердить')