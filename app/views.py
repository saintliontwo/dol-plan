from app import app
from flask import redirect, render_template, request, url_for


@app.route('/')
def get_home():
    """Стартовая страница"""
    return render_template('home.html')


@app.route('/form')
def get_form():
    """Страница с необходимой формой"""
    pass


@app.route('/result')
def get_result():
    """Стартовая с готовым планом"""
    pass