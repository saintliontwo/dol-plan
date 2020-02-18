from application import app
from flask import redirect, render_template, request, url_for
from application.forms import MyForm
import application.plan_generator.app_dol as g


@app.route('/')
def home():
    return render_template('home.html', title="Главная")


@app.route('/form', methods=['GET', 'POST'])
def form():
    form = MyForm(request.form)
    if request.method == 'POST':
        period = request.form.get('period')
        date = request.form.get('date')
        return redirect(url_for('show_result',
                                period=period,
                                date=date))
    return render_template('form.html',
                           title='Ввод данных',
                           form=form)


@app.route('/final', methods=['GET', 'POST'])
def show_result():
    period = request.args.get('period', None)
    date = request.args.get('date', None)
    data_list = g.plan_generator(g.date_parsing(date))
    return render_template('final.html',
                           title='Созданный план',
                           data_list=data_list,
                           period=period,
                           date=date[0:4])                        # нужен только год
