import requests
from datetime import datetime
import os

API_KEY_WEATHER = os.environ['API_KEY_WEATHER']


def create_message(index):
    response = requests.get(f'http://api.weatherapi.com/v1/forecast.json?key={API_KEY_WEATHER}'
                            f'&q=53.41257639604621, 87.28455129798549&days=3&aqi=no&alerts=no&lang=ru').json()
    index_map = {0: 'Сегодня', 1: 'Завтра', 2: 'Послезавтра'}

    day = response['forecast']['forecastday'][index]['date']
    date = datetime.strptime(day, '%Y-%m-%d')
    date_converted = date.strftime('%x %A')

    hours = response['forecast']['forecastday'][index]['hour']

    title = f'<b>{index_map.get(index)} - {date_converted}</b>\n'
    list_of_hours = create_hours(hours)

    return title + list_of_hours


def get_emoji_by_code(code):
    emoji_map = {
        '☀️': [1000],
        '🌤': [1003],
        '☁️': [1006, 1009, 1030, 1135, 1147],
        '🌦': [1063, 1069, 1180, 1186, 1192, 1210, 1216, 1222, 1240, 1243, 1246, 1249, 1252,
              1255, 1258, 1261, 1264],
        '🌧': [1150, 1153, 1183, 1189, 1195, 1204, 1207, 1213, 1219, 1225, 1237],
        '⛈': [1279, 1282],
        '🌩': [1087, 1273, 1276],
    }

    for emoji, codes in emoji_map.items():
        if code in codes:
            return emoji
    return '⛅️'


def create_hours(hours):
    every_second_hour = [hours[index] for index in range(0, len(hours), 2)]
    hour_info = ''
    for hour in every_second_hour:
        date_hour = datetime.strptime(hour['time'], '%Y-%m-%d %H:%M')
        date_hour_converted = date_hour.strftime('%H:%M')
        temperature = hour['temp_c']
        wind = hour['wind_kph']
        emoji = get_emoji_by_code(hour['condition']['code'])
        chance_of_rain = hour['chance_of_rain']
        hour_info += f'{date_hour_converted}: {round(temperature)}&#176;C {emoji} {wind} км/ч {chance_of_rain}% в.о.\n'
    return hour_info
