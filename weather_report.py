from flask import Flask
from data import db_session
from data.weather import Weather
from data.locations import Location
from datetime import date as dt, timedelta as tdt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def find_report(region, date):
    db_session.global_init("db/weather.db")
    db_sess = db_session.create_session()
    query = db_sess.query(Location).filter(Location.name.like(region))
    if query.count() == 0:
        return
    location_id = query[0].id
    if date != "-":
        query = db_sess.query(Weather).filter(Weather.location_id.like(location_id), Weather.date >= date)
    else:
        query = db_sess.query(Weather).filter(Weather.location_id.like(location_id))
    if query.count() == 0:
        return
    return query


def find_reports(region, date_choice):
    results = []
    if date_choice == "На сегодня":
        results.append(find_report(region, dt.today()))
    elif date_choice == "За неделю":
        results.append(find_report(region, dt.today() - tdt(days=6)))
    elif date_choice == "За месяц":
        results.append(find_report(region, dt.today() - tdt(days=29)))
    elif date_choice == "За год":
        results.append(find_report(region, dt.today() - tdt(days=365)))
    else:
        results.append(find_report(region, "-"))
    if any(results):
        return True, results
    else:
        return False, []