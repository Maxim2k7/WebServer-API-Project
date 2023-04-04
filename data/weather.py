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
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    clouds = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    temperature = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    water_temperature = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    precipitation_type = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    precipitation_value = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    wind_direction = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    wind_velocity = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    atmospheric_pressure = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    user = orm.relationship('Location')