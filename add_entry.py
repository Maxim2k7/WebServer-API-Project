from flask import Flask
from data import db_session
from data.weather import Weather
from data.locations import Location

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/weather.db")
    db_sess = db_session.create_session()
    """
    new_report = Weather()
    new_report.location_id = 2
    new_report.date = "01.01.2001"
    new_report.clouds = 1
    new_report.temperature = 100
    new_report.water_temperature = 100
    new_report.precipitation_type = "tacos"
    new_report.precipitation_value = 0
    new_report.wind_direction = "W"
    new_report.wind_speed = 1
    new_report.atmospheric_pressure = 700
    db_sess.add(new_report)
    """
    new_report = Weather()
    new_report.location_id = 1
    new_report.date = "14.07.2017"
    new_report.clouds = 0
    new_report.temperature = 26
    new_report.water_temperature = 20
    new_report.precipitation_type = "rain"
    new_report.precipitation_value = 7
    new_report.wind_direction = "S"
    new_report.wind_speed = 2
    new_report.atmospheric_pressure = 101
    db_sess.add(new_report)
    """
    new_location = Location()
    new_location.name = "Москва"
    new_location.type = "Город"
    new_location.region = "Московская область"
    new_location.latitude = 55.755864
    new_location.longitude = 37.617698
    db_sess.add(new_location)
    """
    db_sess.commit()
    app.run()


if __name__ == '__main__':
    main()