import datetime
import json


def transform_date(date: str) -> datetime:
    """
        Преобразование строковой переменной в обект datetime
        :param date: строковое представление даты %Y-%m-%d;
    """
    year, month, day = (int(i) for i in date.split('-'))
    return datetime.date(year, month, day)


def convert_json(file_path: str):
    """
        Преобразование json-файла в словарь
        :param file_path: строковое представление
    """
    with open(file_path, encoding="utf-8") as file:
        return json.load(file)


def insert_date_info(start_date: datetime):
    """
        Инициализация календарных мероприятий в схеме
        :param start_date: дата начала смены
        :return schema: план с раставленной датой и календарными мероприятиями
    """
    schema = convert_json(r"application\data\schema.json")  # получаем схему нашег плана
    calendar_events = convert_json(r"application\data\calendar_event_list.json")  # получаем словарь календарных событий

    for i in range(0, 21):
        day = start_date + datetime.timedelta(days=i)
        day_info = schema[str(i + 1)]["day description"]
        day_info["date"] = day.strftime("%d.%m")        # строковое представление дня, наприм. 02.10
        day_info["name day"] = day.strftime("%A")       # день недели, напр. Friday
        """условия для присвоения дню календарных событий субботы и пятницы"""
        day_events = schema[str(i + 1)]["events"]
        if i+1 in range(1, 3+1) or i in range(19, 21+1):  # начало или конец смены - календрные события не присваиваются
            continue
        else:  # присвоение календарных событий
            if day_info["name day"] == "Saturday":
                for time_of_day in calendar_events["Saturday"]["events"]:
                    day_events[time_of_day] = calendar_events["Saturday"]["events"][time_of_day]
            elif day_info["name day"] == "Friday":
                for time_of_day in calendar_events["Friday"]["event"]:
                    day_events[time_of_day] = calendar_events["Friday"]["event"][time_of_day]
    return schema


def generate_event(plan: dict, event_list: dict, tof: str):
    """
        :param plan: план с мероприятиями
        :param event_list: словарь с мероприятиями на определенное время суток
        :param tof: time of day - одно из значений списка [evening, afternoon, morning]
    """
    for event in event_list:
        # событие в списке одно
        if "event" in event.keys():
            if len(event["day"]) < 3:       # определенная дата
                plan[event["day"]]["events"][tof] = event["event"][tof]
            elif len(event["day"]) >= 3:    # неопределенная дата
                start, end = [int(num) for num in event["day"].split("-")]
                for date in range(start, end + 1):
                    """>>> место для проверки очередности и последовательности мероприятий <<<"""
                    if plan[str(date)]["events"][tof] is None:      # может не сработать из за приведения типов
                        plan[str(date)]["events"][tof] = event["event"][tof]
                        break # nothings was here
                    else:
                        continue  # continue
        # событие в списке несколько
        elif "events" in event.keys():
            # определенная дата
            if len(event["day"]) < 3:
                for time_of_day in event['events']:  # перебираем все времена суток
                    plan[event["day"]]["events"][time_of_day] = event['events'][time_of_day]
            # неопределенная дата
            elif len(event["day"]) >= 3:
                start, end = [int(n) for n in event["day"].split("-")]  # date districts
                for day in range(start, end + 1):  # iterate for days
                    counter = 0
                    assign = False  # все мероприятия присвоены
                    """>>> место для проверки очередности и последовательности мероприятий <<<"""
                    """проверяем пустые ли мероприятие в течение интересующего нас дня"""
                    for time_of_day in [t for t in event["events"].keys()]:
                        """если время суток мероприятие пустое увеличиваем счетчик, иначе берем следующий день"""
                        if plan[str(day)]["events"][time_of_day] == None:
                            counter += 1
                            """если temp = количеству мероприятий в исходном файле, присваиваем мероприятия дню плана"""
                            if counter == len(event["events"].keys()):
                                for time_of_day in event["events"].keys():
                                    plan[str(day)]["events"][time_of_day] = event["events"][time_of_day]
                                assign = True
                                break
                        else:
                            break
                    if assign:
                        break
    return plan


def generate_unimportant(plan, event_list):
    """ТОЛЬКО ПОТОМУ ЧТО В unimportant_event_list.json в каждом из времен дня только 2! мероприятия"""
    last_evening_event = event_list["evening"][0]
    last_afternoon_event = event_list["afternoon"][0]
    last_morning_event = event_list["morning"][0]
    for day in plan.keys():    # iterate final_plan
        for tod in event_list.keys():    # iterate schema
            """universal"""
            # если событие есть ->  дальше
            if plan[day]["events"][tod] is not None:
                continue
            # исключение
            if plan[day]["events"]["evening"] == 'танцевальный марафон':
                last_evening_event = "дискотека"
            # если мероприятие в списке равно неважному_1 оно последнее во временном файле
            elif plan[day]["events"][tod] == event_list[tod][0]:
                if tod == "evening":
                    last_evening_event = event_list[tod][0]
                elif tod == "afternoon":
                    last_afternoon_event = event_list[tod][0]
                elif tod == "morning":
                    last_morning_event = event_list[tod][0]
            # если мероприятие в списке равно неважному_2 оно последнее во временном файле
            elif plan[day]["events"][tod] == event_list[tod][1]:
                if tod == "evening":
                    last_evening_event = event_list[tod][1]
                elif tod == "afternoon":
                    last_afternoon_event = event_list[tod][1]
                elif tod == "morning":
                    last_morning_event = event_list[tod][1]
            # если мероприятие в списке нет
            elif plan[day]["events"][tod] is None:
                if tod == "evening":
                    # присваиваем отличное от последнего в списке мероприятия, перезаписываем временное
                    if last_evening_event == event_list[tod][0]:
                        plan[day]["events"][tod] = event_list[tod][1]
                        last_evening_event = event_list[tod][1]
                    else:
                        plan[day]["events"][tod] = event_list[tod][0]
                        last_evening_event = event_list[tod][0]
                elif tod == "afternoon":
                    if last_afternoon_event == event_list[tod][0]:
                        plan[day]["events"][tod] = event_list[tod][1]
                        last_afternoon_event = event_list[tod][1]
                    else:
                        plan[day]["events"][tod] = event_list[tod][0]
                        last_afternoon_event = event_list[tod][0]
                elif tod == "morning":
                    if last_morning_event == event_list[tod][0]:
                        plan[day]["events"][tod] = event_list[tod][1]
                        last_morning_event = event_list[tod][1]
                    else:
                        plan[day]["events"][tod] = event_list[tod][0]
                        last_morning_event = event_list[tod][0]
    return plan


def generate_plan(date):
    # copy schema and insert calendar days
    plan = insert_date_info(date)  #
    # evening
    evening_events_list = r"application\data\evening_event_list.json"
    evening_plan = generate_event(plan, convert_json(evening_events_list), tof="evening")
    # afternoon
    afternoon_events_list = r"application\data\afternoon_event_list.json"
    afternoon_plan = generate_event(evening_plan, convert_json(afternoon_events_list), tof="afternoon")
    # morning
    morning_event_list = r"application\data\morning_event_list.json"
    morning_plan = generate_event(afternoon_plan, convert_json(morning_event_list), tof="morning")
    # unimportant
    unimportant_event_list = r"application\data\unimportant_event_list.json"
    FINAL_PLAN = generate_unimportant(morning_plan, convert_json(unimportant_event_list))
    # print(plan)
    return FINAL_PLAN

