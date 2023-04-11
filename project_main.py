# -*- coding: utf-8 -*-
from flask import Flask, render_template
from weather_report import find_report

app = Flask(__name__)

# Константы
weather_params = ["Облачность: ", "Температура воздуха: ", "Температура воды: ", "Тип осадков: ", "Количество осадков: ",
                  "Направление ветра: ", "Скорость ветра: ", "Атмосферное давление: "]
measuring_units = ["", "°C", "°C", "", "мм", "", "м/c", "мм рт. ст."]


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')


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