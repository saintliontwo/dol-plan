from app import app
from .main import generate_plan, transform_date, remain_main_event
from flask import redirect, render_template, request, url_for
from .forms import MyForm


@app.route('/')
def get_home():
    return render_template('home.html')


@app.route('/form', methods=['GET', 'POST'])
def get_form():
    form = MyForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        return redirect(url_for('get_result',
                                period=request.form.get("period"),
                                date=request.form.get("date"),
                                main_event=request.form.get("main_event")),
                        code=302)
    return render_template('form.html', form=form)


@app.route('/result')
def get_result():
    # args
    period = request.args.get("period")
    main_event = request.args.get("main_event")
    start_date=request.args.get("date")
    
    plan = generate_plan(transform_date(start_date))
    return render_template("result.html",
                           plan=remain_main_event(plan, main_event),
                           period=period,
                           year=start_date[:4])
