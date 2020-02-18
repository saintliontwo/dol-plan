# dol-plan
Программа для детского оздоровительного лагеря ОРЛЕНОК - версия 2.0.4

## description
Вторая версия приложения генерирует план смены вечерених мероприятий с web-интерфейсом 

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
├── application
│   ├── plan_generator
│   │   ├── __init__.py
│   │   ├── app_dol.py
│   │   └── events.csv
│   ├── static
│   │   ├── css
│   │   │   └── index.css
│   ├── templates
│   │   ├── base.html
│   │   ├── final.html
│   │   ├── form.html
│   │   └── home.html
│   ├── __init__.py
│   ├── forms.py
│   └── views.py
├── config
├── requiremints.txt
└── run.py
```

## how to use
Cкрипт запускается инлайн-командой ```python app.py```. На компьютере должен быть предустановлен python 3.7 (*протестировано*) с зависимостями из файла `requirements.txt`. Необходимо следовать инструкциям и перейти на страницу в браузере (http://127.0.0.1:5000/). Следуйте инструкциям веб-страницы. Результатом работы станет возможность распечатать готовый план в виде html-страницы в которой в упорядоченном формате расположились вечерние мероприятия.
