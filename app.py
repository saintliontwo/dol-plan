import datetime
import csv
import json
import os


__csvfile = 'events.csv'


def date_parsing() -> datetime.date:
    """Метод подразумевает корректный ввод даты. Обработка ошибок не предусмотрена.
        Обязательно изменить механизм парсинга при помощи модуля re."""

    answer = input("Введите дату начала смены в формате \'день.месяц.год\': ")
    day, month, year = (int(i) for i in answer.split('.'))
    date = datetime.date(year, month, day)
    return date


def _generate(gap: str, planed_dict: dict) -> int:
    """Генерирует дату мероприятия среди свободных чисел из заданного диапозона."""

    if len(gap) < 3 and gap != '0':                                             # мероприятия с конкретной датой
        return int(gap)
    if gap != '0':                                                              # мероприятия с диапозоном дат
        start, end = [int(i) for i in gap.split(sep='-')]
    else:                                                                       # мероприятия не имеющие приоритета
        start, end = 1, 21
    for day in range(start, end+1):
        if day not in planed_dict.keys():
            return day
        else:
            continue


def _timestamp_translate(date: datetime, num: int) -> str:
    """Возвращает день смены в формате строки. Date - дата начала смены, Num - порядковый день смены.
        Отрефакторить при помощи модуля locale."""

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
    ru_week = DAYS_DICT['day_week'][date_str('%A')]
    ru_month = DAYS_DICT['months'][date_str('%B')]
    return '{0} {1}, {2}'.format(date_str('%d'), ru_month, ru_week)


def plan_generator(file_path: csv, start_date: datetime) -> list:
    """Прочитывает csv-файл с данными о проведении мероприятий"""

    future_dict = dict()
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)                                                                # пропускаем заголовки
        for row in reader:                                                          # считываем данные из csv-файл
            event, day = row[0], row[1]
            gen_day = _generate(day, future_dict)                                   # функция генерирует дату
            future_dict[gen_day] = {'день': _timestamp_translate(start_date, gen_day),
                                    'мероприятие': event,}
    return {k: future_dict[k] for k in sorted(future_dict)}


def save_json(plan: dict):
    """Функция для сохранения плана в файл формата json(?)"""

    with open('evening_plan.json', 'w') as file:  # dump
        json.dump(plan, file, ensure_ascii=False, indent=2)
    print('Планы вечерних мероприятий создан и сохранен в директории - {}\n'
          'Имя файла - evening_plan.json'.format(os.getcwd()))


if __name__ == '__main__':
    start_date = date_parsing()
    plan = plan_generator(__csvfile, start_date)
    save_json(plan)