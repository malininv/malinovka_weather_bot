import requests
from datetime import datetime
import os

API_KEY_WEATHER = os.environ['API_KEY_WEATHER']
DAYS_WEATHER = 3


def get_weekday(number: int) -> str:
    weekday_map = {0: 'Понедельник', 1: 'Вторник', 2: 'Среда', 3: 'Четверг', 4: 'Пятница', 5: 'Суббота',
                   6: 'Воскресенье'}
    return weekday_map.get(number)


def get_json_from_api():
    return requests.get(f'http://api.weatherapi.com/v1/forecast.json?key={API_KEY_WEATHER}'
                        f'&q=53.41257639604621, 87.28455129798549&days={DAYS_WEATHER}&aqi=no&alerts=no&lang=ru').json()


def get_converted_day_and_weekday(date: str) -> (str, str):
    converted_day_date = datetime.strptime(date, '%Y-%m-%d')
    weekday = get_weekday(converted_day_date.weekday())
    return converted_day_date.strftime('%d.%m.%Y '), weekday


def get_relative_date(index):
    relative_date_map = {0: 'Сегодня', 1: 'Завтра', 2: 'Послезавтра'}
    return relative_date_map.get(index)


def create_message(index):
    response = get_json_from_api()
    forecast = response['forecast']['forecastday'][index]
    date, hours = forecast['date'], forecast['hour']
    day, week_day = get_converted_day_and_weekday(date)
    relative_date = get_relative_date(index)
    title = f'<b>{relative_date} - {day} {week_day}</b>\n'
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


def get_converted_hour(hour: str) -> str:
    converted_hour = datetime.strptime(hour, '%Y-%m-%d %H:%M')
    return converted_hour.strftime('%H:%M')


def create_hours(hours):
    every_second_hour = [hours[index] for index in range(0, len(hours), 2)]
    hour_info = ''
    for hour in every_second_hour:
        hour_converted = get_converted_hour(hour['time'])
        temperature = hour['temp_c']
        wind = hour['wind_kph']
        emoji = get_emoji_by_code(hour['condition']['code'])
        chance_of_rain = hour['chance_of_rain']
        hour_info += f'{hour_converted}: {round(temperature)}&#176;C {emoji} {wind} км/ч {chance_of_rain}% в.о.\n'
    return hour_info
