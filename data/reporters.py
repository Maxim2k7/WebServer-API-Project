import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class Reporter(SqlAlchemyBase):
    __tablename__ = 'reporters'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    login = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
