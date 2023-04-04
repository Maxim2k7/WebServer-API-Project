from flask import Flask
from data import db_session
from data.locations import Location

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/weather.db")
    db_sess = db_session.create_session()
    new_location = Location()
    new_location.name = "Воронеж"
    new_location.type = "Город"
    new_location.region = "Воронежская область"
    new_location.latitude = 51.660781
    new_location.longitude = 39.200296
    db_sess.add(new_location)
    db_sess.commit()
    app.run()


if __name__ == '__main__':
    main()