# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect
from weather_report import find_report
from forms.find_report import SearchForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

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
@app.route('/reporter/enter')
def reporter_enter():
    return render_template('form.html')

# Добавление информации
@app.route('/reporter/edit')
def reporter_main():
    return render_template('reporter.html')


if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1")