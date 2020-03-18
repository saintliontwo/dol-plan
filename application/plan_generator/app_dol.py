"""app_dol_v.2.0.4"""

import datetime
import csv


def date_parsing(date: str) -> datetime:
    """Метод подразумевает корректный ввод даты. Обработка ошибок не предусмотрена."""

    year, month, day = (int(i) for i in date.split('-'))
    date = datetime.date(year, month, day)
    return date


def _generate(gap: str, future_plan: list) -> int:
    """Генерирует дату мероприятия среди свободных чисел из заданного диапозона."""

    if len(gap) < 3 and gap != '0':                                             # мероприятия с конкретной датой
        return int(gap)
    if gap != '0':                                                              # мероприятия с диапозоном дат
        start, end = [int(i) for i in gap.split(sep='-')]
    else:                                                                       # мероприятия не имеющие приоритета
        start, end = 1, 21
    for day in range(start, end+1):
        if day not in [days['day']['numeric'] for days in future_plan]:                                              #  2.0.0
            return day
        else:
            continue


def date_translate(date: datetime, num: int) -> str:
    """Возвращает день смены в формате строки(прим. "3 января, пятница").
        date - дата начала смены, num - порядковый день смены. Отрефакторить при помощи модуля locale.
    """

    DAYS_DICT = {
                'day_week': {
                         'Monday': 'Понедельник',
                         'Tuesday': 'Вторник',
                         'Wednesday': 'Среда',
                         'Thursday': 'Четверг',
                         'Friday': 'Пятница',
                         'Saturday': 'Суббота',
                         'Sunday': 'Воскресенье'
                        },
                'months': {'December': 'Декабря',
                           'January': 'Января',
                           'February': 'Февраля',
                           'March': 'Марта',
                           'April': 'Апреля',
                           'May': 'Мая',
                           'June': 'Июня',
                           'July': 'Июля',
                           'August': 'Августа',
                           'September': 'Сентября',
                           'October': 'Октября',
                           'November': 'Ноября',
                        }
                }
    date_str = (date + datetime.timedelta(num-1)).strftime
    ru_weekday = DAYS_DICT['day_week'][date_str('%A')]
    ru_month = DAYS_DICT['months'][date_str('%B')]
    return '{0} {1}, {2}'.format(date_str('%d'), ru_month, ru_weekday)


def plan_generator(start_date: datetime) -> list:
    """Прочитывает csv-файл с данными о проведении мероприятий"""

    file_path = r'application\plan_generator\events.csv' # месторасположение файла
    future_plan = list()
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)                                                                # пропускаем заголовки
        for row in reader:                                                          # считываем данные из csv-файл
            event, day = row[0], row[1]
            gen_day = _generate(day, future_plan)                                   # функция генерирует дату
            future_plan.append({'day': {'numeric': gen_day,
                                        'date': date_translate(start_date, gen_day)},
                                'event': event
                                })
    return sorted(future_plan, key=lambda k: k['day']['numeric'])                   # сортируем список дней(словарей)
