# -*- coding: utf-8 -*-
import datetime

from flask import Flask, render_template, redirect, request
from flask_login import login_user, LoginManager, login_required, logout_user
from forms.reporter import RegisterForm, LoginForm
from data import db_session
from data.reporters import Reporter
from weather_report import find_report
from data.weather import Weather
from forms.find_report import SearchForm
from data.locations import Location
from flask_restful import Api
import data.weather_resources
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

api = Api(app)
api.add_resource(data.weather_resources.WeatherListResource, '/api/weather')
api.add_resource(data.weather_resources.WeatherResource, '/api/weather/<int:weather_id>')

login_manager = LoginManager()
login_manager.init_app(app)


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
        if not (ok):
            return render_template('home_page.html', title='Поиск',
                                   form=form,
                                   message="Такие данные отсутствуют")
        return redirect(f'/weather/{form.city.data}/{form.date.data}')
    return render_template('home_page.html', title='Поиск', form=form)


@app.route('/weather/<region>/<date>')
def weather_main(region, date):
    ok, result = find_report(region, date)
    data = [result.clouds, result.temperature, result.water_temperature, result.precipitation_type,
            result.precipitation_value, result.wind_direction, result.wind_velocity, result.atmospheric_pressure]
    return render_template('location.html', found=ok, place=region, data=data, headers=weather_params,
                           units=measuring_units, date=date)


# Загрузка профиля пользователя
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Reporter).get(user_id)


# Вход для репортеров
@app.route('/reporter/enter', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        reporter = db_sess.query(Reporter).filter(Reporter.email == form.login.data).first()
        if not reporter:
            reporter = db_sess.query(Reporter).filter(Reporter.login == form.login.data).first()
        if reporter and reporter.check_password(form.password.data):
            login_user(reporter, remember=form.remember_me.data)
            print(form.remember_me.data)
            return redirect("/reporter/edit")
        return render_template('authorization.html',
                               message="Неправильный логин/пароль",
                               form=form)
    return render_template('authorization.html', title='Авторизация', form=form)


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


# Основая страница репортера
# именно здесь заносятся данные о погоде
@app.route('/reporter/edit', methods=['POST', 'GET'])
@login_required
def reporter_main():
    if request.method == 'GET':
        return render_template('reporter.html')
    elif request.method == 'POST':
        db_sess = db_session.create_session()
        weather = Weather(
            location_id=int(db_sess.query(Location.id).filter(Location.name == request.form['location']).first()[0]),
            date=request.form['date'],
            clouds=request.form['clouds'],
            temperature=request.form['temperature'],
            water_temperature=request.form['water_temperature'],
            precipitation_type=request.form['precipitation_type'],
            precipitation_value=request.form['precipitation_value'],
            wind_direction=request.form['wind_direction'],
            wind_velocity=request.form['wind_velocity'],
            atmospheric_pressure=request.form['atmospheric_pressure'],
        )
        db_sess.merge(weather)
        db_sess.commit()
        return redirect('/reporter/edit/success', page='/reporter/edit')

# окно, сообщающее об удачном сохранении данных
@app.route('/reporter/edit/success')
def success():
    return render_template("success.html")

#
@app.route('/reporter/load', methods=['POST', 'GET'])
def load():
    if request.method == 'GET':
        return render_template("load.html")
    elif request.method == 'POST':
        js = request.files['file']
        res = json.loads(js.read())['weather']
        db_sess = db_session.create_session()
        try:
            weather = Weather(
                location_id=res['location_id'],
                date=res['date'],
                clouds=res['clouds'],
                temperature=res['temperature'],
                water_temperature=res['water_temperature'],
                precipitation_type=res['precipitation_type'],
                precipitation_value=res['precipitation_value'],
                wind_direction=res['wind_direction'],
                wind_velocity=res['wind_velocity'],
                atmospheric_pressure=res['atmospheric_pressure'],
            )
        except:
            return render_template("fail.html", page='/reporter/load')
        db_sess.merge(weather)
        db_sess.commit()
        return render_template("success.html", page='/reporter/load')

# выход из профиля пользователя
@app.route('/reporter/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

# докумантация к API
@app.route('/api/documentation')
def api_documentation():
    return render_template('api_doc.html')

if __name__ == "__main__":
    main()
