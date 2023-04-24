from flask import Flask
from data import db_session
from data.weather import Weather
from datetime import datetime
from random import randint, choice

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    # Генерация случайной информации для заполнения БД
    db_session.global_init("db/weather.db")
    db_sess = db_session.create_session()
    for i in range(1000):
        new_report = Weather()
        new_report.location_id = randint(1, 3)
        new_report.date = datetime.strptime(f"{randint(2001, 2023)}-0{randint(1, 9)}-{randint(10, 28)}",
                                            '%Y-%m-%d').date()
        new_report.clouds = randint(0,2)
        new_report.temperature = randint(-50, 50)
        new_report.water_temperature = new_report.temperature + randint(-10, 10)
        new_report.precipitation_type = choice(["Дождь", "Снег", "Град", "Нет осадков"])
        new_report.precipitation_value = randint(1, 100) if new_report.precipitation_type != "Нет осадков" else 0
        new_report.wind_direction = choice(["N", "NE", "E", "SE", "S", "SW", "W", "NW", "Нет ветра"])
        new_report.wind_velocity = randint(1, 10) if new_report.wind_direction != "Нет ветра" else 0
        new_report.atmospheric_pressure = randint(95, 106)
        if new_report.date <= datetime.today().date():
            db_sess.add(new_report)
    db_sess.commit()
    app.run()


if __name__ == '__main__':
    main()