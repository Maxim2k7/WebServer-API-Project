# -*- coding: utf-8 -*-
from flask import Flask, render_template

app = Flask(__name__)


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

# Добавление информации
@app.route('/reporter/edit')
def reporter_main():
    return render_template('reporter.html')


if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1")