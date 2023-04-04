from flask import Flask
from data.db_session import global_init, create_session
from data.weather import Weather
from data.locations import Location

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def find_by_location(region):
    global_init("weather.db")
    db_sess = create_session()
    for i in db_sess.query(Weather).filter(Weather.location.like(region)):
        print(i)
