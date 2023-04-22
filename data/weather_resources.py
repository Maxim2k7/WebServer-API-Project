from flask import abort, jsonify, request
from data import db_session
from data.weather import Weather
from flask_restful import abort, Api, Resource
from data.reqparser import parser

class WeatherResource(Resource):
    def get(self, weather_id):
        abort_if_weather_not_found(weather_id)
        session = db_session.create_session()
        weather = session.query(Weather).get(weather_id)
        return jsonify(weather.as_dict())

    def delete(self, weather_id):
        abort_if_weather_not_found(weather_id)
        session = db_session.create_session()
        weather = session.query(Weather).get(weather_id)
        session.delete(weather)
        session.commit()
        return jsonify({'success': 'OK'})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        weather = Weather(
            location_id=args['location'],
            date=args['date'],
            clouds=args['clouds'],
            temperature=args['temperature'],
            water_temperature=args['water_temperature'],
            precipitation_type=args['precipitation_type'],
            precipitation_value=args['precipitation_value'],
            wind_direction=args['wind_direction'],
            wind_velocity=args['wind_velocity'],
            atmospheric_pressure=args['atmospheric_pressure'],
        )
        session.add(weather)
        session.commit()
        return jsonify({'success': 'OK'})

def abort_if_weather_not_found(weather_id):
    session = db_session.create_session()
    news = session.query(Weather).get(weather_id)
    if not news:
        abort(404, message=f"Weather {weather_id} not found")