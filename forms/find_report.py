from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    city = StringField('Где хотите посмотреть погоду (город)?', validators=[DataRequired()])
    date = StringField('Дата на которую хотите посмотреть погоду', validators=[DataRequired()])
    submit = SubmitField('Найти')