import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Weather(SqlAlchemyBase):
    __tablename__ = 'weather'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    location_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("locations.id"))
    date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.date.today())
    clouds = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    temperature = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    water_temperature = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    precipitation_type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    precipitation_value = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    wind_direction = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    wind_speed = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    atmospheric_pressure = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    location = orm.relationship('Location')