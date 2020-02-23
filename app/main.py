"""greedy вариант генерации плана"""


import datetime
import json


def transform_date(date: str) -> datetime:
    """
        Преобразование строковой переменной в обект datetime
        :param date: строковое представление даты %Y-%m-%d;
    """
    year, month, day = (int(i) for i in date.split('-'))
    return datetime.date(year, month, day)


def convert_json(file_path: str) -> dict:
    """
        Выгрузка и преобразование json-файла в словарь
        :param file_path: строковое представление
    """
    with open(file_path, encoding="utf-8-sig", ) as file:
        return json.load(file)


def localize_day_name(day_number: str) -> str:
    """
        :param day_number: представление дня недели datetime.strftime("%w")
        :return: день недели в необходимом формате
    """
    local_day_dict = {
        "0": "пн",
        "1": "вт",
        "2": "ср",
        "3": "чт",
        "4": "пт",
        "5": "сб",
        "6": "вс",
    }
    return local_day_dict[day_number]


def insert_date_info(start_date: datetime) -> dict:
    """
        Инициализация календарных мероприятий в схеме.
        :param start_date: дата начала смены
        :return schema: план с раставленной датой и календарными мероприятиями
    """
    schema = convert_json(r"application\data\schema.json")                          # скелет плана
    calendar_events = convert_json(r"application\data\calendar_event_list.json")    # календарные события

    for i in range(0, 21):
        day = start_date + datetime.timedelta(days=i)                   # порядковый день смены
        day_events = schema[str(i + 1)]["events"]                       # блок с событиями
        day_info = schema[str(i + 1)]["day description"]                # блок с информацией
        day_info["date"] = day.strftime("%d.%m")                        # строковое представление дня (02.10)
        day_info["name day"] = localize_day_name(day.strftime("%w"))    # день недели (пн)

        if i+1 in range(1, 3+1) or i in range(19, 21+1):    # в начале/конце смены календрные события не присваиваются
            continue
        else:                                               # присвоение календарных событий
            name_day = day_info["name day"]
            if name_day == "Saturday":
                for tod in calendar_events[name_day]["events"]:
                    day_events[tod] = calendar_events[name_day]["events"][tod]
            elif name_day == "Friday":
                for tod in calendar_events[name_day]["event"]:
                    day_events[tod] = calendar_events[name_day]["event"][tod]
    return schema


def generate_event(plan: dict, event_list: dict, tod: str) -> dict:
    """
        Функция распределеяет мероприятие(-ия) по дням.
        :param plan: план-скелет
        :param event_list: словарь с мероприятиями на выбранное время суток
        :param tod: time of day - значений времени суток: evening/afternoon/morning
        :return new_plan: новый план сгенерированных событий
    """
    new_plan = plan
    for current_day in event_list:
        if "event" in current_day.keys():                                             # мероприятие одно
            if len(current_day["day"]) < 3:                                           # мероприятие имеет определенную дату
                new_plan[current_day["day"]]["events"][tod] = current_day["event"][tod]
            elif len(current_day["day"]) >= 3:                                        # мероприятие НЕ имеет определенную дату
                start, end = [int(num) for num in current_day["day"].split("-")]
                for date in range(start, end + 1):
                    """>>> место для проверки очередности и последовательности мероприятий <<<"""
                    if new_plan[str(date)]["events"][tod] is None:
                        new_plan[str(date)]["events"][tod] = current_day["event"][tod]
                        break
                    else:
                        continue  # continue
        elif "events" in current_day.keys():                                          # событий в списке несколько
            if len(current_day["day"]) < 3:                                           # мероприятия имеют определенную дату
                for tod_ in current_day['events']:
                    new_plan[current_day["day"]]["events"][tod_] = current_day['events'][tod_]
            elif len(current_day["day"]) >= 3:                                        # мероприятия НЕ имеют определенной даты
                event_numbers = len(current_day["events"].keys())  # количество мероприятий необходимое для присвоение дню
                start, end = [int(n) for n in current_day["day"].split("-")]
                for day in range(start, end + 1):
                    counter = 0
                    assign = False                                                    # все мероприятия из списка присвоены
                    """>>> место для проверки очередности и последовательности мероприятий <<<"""
                    """
                        В этой части кода мы проверяем не заняты ли времена суток(tod_) из исходного списка(current_day) 
                        на конкретный день(day) в новом плане(new_plan). Если время суток на определенную дату в новом 
                        плане пустое, счетчик увеличивается. Как только счетчик равен количеству мероприятий(event_numbers) 
                        которые нам необходимо вставить, мы присваеваем данному дню мероприятия из списка current_day.
                    """
                    for tod_ in current_day["events"].keys():
                        if new_plan[str(day)]["events"][tod_] is None:
                            counter += 1
                            if counter == event_numbers:
                                for _tod in current_day["events"].keys():
                                    new_plan[str(day)]["events"][_tod] = current_day["events"][_tod]
                                assign = True
                                break
                        else:
                            break
                    if assign:
                        break
    return new_plan


def generate_unimportant(plan, event_list):
    """
        Функция распределяет оставшиеся мероприятия по дням.
                    ! Костыль: реализация функции возможна только потому что в unimportant_event_list.json !
                                        в каждом из времен дней только 2! мероприятия
        :param plan: план-скелет
        :param event_list: словарь с мероприятиями
        :return new_plan: новый план сгенерированных событий
    """
    new_plan = plan
    last_event = {"evening": event_list["evening"][0],
                  "afternoon": event_list["afternoon"][0],
                  "morning": event_list["morning"][0]}
    for current_day in new_plan.keys():                                                             # конкретный день
        event = new_plan[current_day]["events"]  # блок мероприятий
        for tod in event.keys():
            """
                Если мероприятие уже есть в плане мы проверяем является ли оно последним в списке и меняем его значение
                если это необходимо. Также присутсвует исключение.
            """
            if event[tod] is not None:
                if event[tod] in event_list[tod]:                   # одно из планируемых мероприяйтий
                    last_event[tod] = event[tod]
                if event["evening"] == 'танцевальный марафон':      # исключение
                    last_event["evening"] = "дискотека"
                else:
                    pass
                continue
            elif event[tod] is None:
                 if last_event[tod] == event_list[tod][0]:
                     event[tod] = event_list[tod][1]
                 else:
                     event[tod] = event_list[tod][0]
                 last_event[tod] = event[tod]
    return new_plan


def generate_plan(date: datetime):
    """:param date: день начала смены"""
    # copy schema and insert calendar days
    plan = insert_date_info(date)  #
    # evening
    evening_events_list = r"application\data\evening_event_list.json"
    evening_plan = generate_event(plan, convert_json(evening_events_list), tod="evening")
    # afternoon
    afternoon_events_list = r"application\data\afternoon_event_list.json"
    afternoon_plan = generate_event(evening_plan, convert_json(afternoon_events_list), tod="afternoon")
    # morning
    morning_event_list = r"application\data\morning_event_list.json"
    morning_plan = generate_event(afternoon_plan, convert_json(morning_event_list), tod="morning")
    # unimportant
    unimportant_event_list = r"application\data\unimportant_event_list.json"
    FINAL_PLAN = generate_unimportant(morning_plan, convert_json(unimportant_event_list))
    # print(plan)
    return FINAL_PLAN
