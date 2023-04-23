from requests import get, post, put, delete

# создание новости
print(post('http://127.0.0.1:8080/api/weather', json={
    'location_id': 1,
    'date': '27.04.23',
    'clouds': 'NO',
    'temperature': 12,
    'water_temperature': 11,
    'precipitation_type': 'rain',
    'precipitation_value': '900',
    'wind_direction': 'EAST',
    'wind_velocity': 90,
    'atmospheric_pressure': 765}).json())

# получение полного списка всех репортов погоды
print(get('http://127.0.0.1:8080/api/weather').json())

# получение информации о 1 репорте погоды
print(get('http://127.0.0.1:8080/api/weather/1').json())

# удаление новости под номером 1
print(delete('http://127.0.0.1:8080/api/weather/1').json())
