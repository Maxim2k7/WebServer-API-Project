# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect
from forms.reporter import RegisterForm
from data import db_session
from data.reporters import Reporter

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init('db/weather.db')
    app.run(port=8080, host="127.0.0.1", debug=True)


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')


@app.route('/weather/<region>')
def weather_main(region):
    return render_template('location.html', place=region)


# Добавление новой записи о погоде
# Вход
@app.route('/reporter/enter')
def reporter_enter():
    return render_template('form.html')


# Регистрация погодного репортера
@app.route('/reporter/registration', methods=['GET', 'POST'])
def reporter_registration():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(Reporter).filter(Reporter.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Пользователь с такой почтой уже зарегистрирован")
        if db_sess.query(Reporter).filter(Reporter.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Данный логин уже занят")

        reporter = Reporter(
            name=form.name.data,
            surname=form.surname.data,
            login=form.surname.data,
            email=form.email.data,
        )
        reporter.set_password(form.password.data)
        db_sess.add(reporter)
        db_sess.commit()
        return redirect('/reporter/enter')
    return render_template('registration.html', title='Регистрация', form=form)


# Добавление информации
@app.route('/reporter/edit')
def reporter_main():
    return render_template('reporter.html')


if __name__ == "__main__":
    main()
