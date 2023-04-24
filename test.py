from requests import get, post, put, delete

# создание новости
print(post('http://127.0.0.1:8080/api/weather', json={
    'location_id': 1,
    'date': '2023-04-24',
    'clouds': 1,
    'temperature': 12,
    'water_temperature': 11,
    'precipitation_type': 'rain',
    'precipitation_value': 900,
    'wind_direction': 'E',
    'wind_velocity': 90,
    'atmospheric_pressure': 765}).json())

# получение первых 30 репортажей
print(get('http://127.0.0.1:8080/api/weather').json()['weather'][:30])

# получение информации о 4 репорте погоды
print(get('http://127.0.0.1:8080/api/weather/4').json())

# удаление новости под номером 4
print(delete('http://127.0.0.1:8080/api/weather/4').json())
