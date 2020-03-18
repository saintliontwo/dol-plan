# dol-plan
Программа для детского оздоровительного лагеря ОРЛЕНОК - версия 3.0.0

## description
Третья версия приложения генерирует план смены со всеми мероприятиями(утренними, дневными, вечерними) в web-интерфейсе 

## stack 
Python, Flask, HTML, CSS

## requirements

```
Flask==1.1.1
FLASK-WTF==0.12.2
Jinjia2==2.10.3
Werkzeug==0.16.0
wtforms==2.2.1
```

## package

```
dol_plan
├── app
│   ├── data
│   │   ├── afternoon_event_list.json
│   │   ├── calendar_event_list.json
│   │   ├── evening_event_list.json
│   │   ├── morning_event_list.json
│   │   ├── schema.json
│   │   ├── unimportant_event_list.json
│   ├── static
│   │   └── style.css
│   ├── templates
│   │   ├── base.html
│   │   ├── final.html
│   │   ├── form.html
│   │   └── home.html
│   ├── __init__.py
│   ├── forms.py
│   ├── main.py
│   └── views.py
├── README.md
├── config
├── requiremints.txt
└── run.py
```

## how to use
Cкрипт запускается инлайн-командой ```python app.py```. На компьютере должен быть предустановлен python 3.7 (*протестировано*) с зависимостями из файла `requirements.txt`. Необходимо следовать инструкциям и перейти на страницу в браузере (http://127.0.0.1:5000/). Следуйте инструкциям веб-страницы. Результатом работы станет возможность распечатать готовый план в виде html-страницы в которой в упорядоченном формате все мероприятия.
