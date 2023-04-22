from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('location_id', required=True, type=int)
parser.add_argument('date', required=True)
parser.add_argument('clouds', required=True)
parser.add_argument('temperature', required=True, type=int)
parser.add_argument('water_temperature', required=True, type=int)
parser.add_argument('precipitation_type', required=True)
parser.add_argument('precipitation_value', required=True, type=int)
parser.add_argument('wind_direction', required=True)
parser.add_argument('wind_velocity', required=True, type=int)
parser.add_argument('atmospheric_pressure', required=True, type=int)
