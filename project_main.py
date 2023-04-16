# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect
from flask_login import login_user
from forms.reporter import RegisterForm, LoginForm
from data import db_session
from data.reporters import Reporter
from weather_report import find_report
from forms.find_report import SearchForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init('db/weather.db')
    app.run(port=8080, host="127.0.0.1", debug=True)


# Константы
weather_params = [("Облачность: ", True), ("Температура воздуха: ", False), ("Температура воды: ", False),
                  ("Тип осадков: ", False), ("Количество осадков: ", False), ("Направление ветра: ", False),
                  ("Скорость ветра: ", False), ("Атмосферное давление: ", False)]
measuring_units = ["", "°C", "°C", "", "мм", "", "м/c", "мм рт. ст."]


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        ok, result = find_report(form.city.data, form.date.data)
        if not(ok):
            return render_template('home_page.html', title='Поиск',
                                   form=form,
                                   message="Такие данные отсутствуют")
        return redirect(f'/weather/{form.city.data}/{form.date.data}')
    return render_template('home_page.html', title='Поиск', form=form)


@app.route('/weather/<region>/<date>')
def weather_main(region, date):
    ok, result = find_report(region, date)
    data = [result.clouds, result.temperature, result.water_temperature, result.precipitation_type,
            result.precipitation_value, result.wind_direction, result.wind_speed, result.atmospheric_pressure]
    return render_template('location.html', found=ok, place=region, data=data, headers=weather_params,
                           units=measuring_units, date=date)


# Добавление новой записи о погоде
# Вход
@app.route('/reporter/enter', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


# Регистрация погодного репортера
@app.route('/reporter/registration', methods=['GET', 'POST'])
def reporter_registration():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(Reporter).filter(Reporter.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Пользователь с такой почтой уже зарегистрирован")
        if db_sess.query(Reporter).filter(Reporter.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Данный логин уже занят")

        reporter = Reporter(
            name=form.name.data,
            surname=form.surname.data,
            login=form.surname.data,
            email=form.email.data,
        )
        reporter.set_password(form.password.data)
        db_sess.add(reporter)
        db_sess.commit()
        return redirect('/reporter/enter')
    return render_template('registration.html', title='Регистрация', form=form)


# Добавление информации
@app.route('/reporter/edit')
def reporter_main():
    return render_template('reporter.html')


if __name__ == "__main__":
    main()
