from flask import Flask
from data import db_session
from data.weather import Weather
from data.locations import Location

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def find_report(region, date):
    db_session.global_init("db/weather.db")
    db_sess = db_session.create_session()
    query = db_sess.query(Location).filter(Location.name.like(region))
    if query.count() == 0:
        return False, Weather()
    location_id = query[0].id
    query = db_sess.query(Weather).filter(Weather.location_id.like(location_id), Weather.date.like(date))
    if query.count() == 0:
        return False, Weather()
    result = query[0]
    return True, result
