from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired
from data import db_session
from data.locations import Location

date_choices = ["На сегодня", "За неделю", "За месяц", "За год", "За всё время"]


class SearchForm(FlaskForm):
    db_session.global_init("db/weather.db")
    db_sess = db_session.create_session()
    city = SelectField('Где хотите посмотреть погоду?',
                       choices=sorted([i.name for i in db_sess.query(Location).filter()]), validators=[DataRequired()])
    date = SelectField('За какой период?', choices=date_choices, validators=[DataRequired()])
    submit = SubmitField('Найти')