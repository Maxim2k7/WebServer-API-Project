import sqlalchemy
from .db_session import SqlAlchemyBase


class Location(SqlAlchemyBase):
    __tablename__ = 'locations'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    region = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    latitude = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    longitude = sqlalchemy.Column(sqlalchemy.Float, nullable=True)