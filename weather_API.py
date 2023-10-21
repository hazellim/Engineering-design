import datetime as dt
import requests

api_key = '49149c3c44b44dd269d4ccd896fba3f6'

user_input = input('Enter city: ')

weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=metric&APPID={api_key}")

if weather_data.json()['cod'] == '404':
    print('No city found')
else:
    weather = weather_data.json()['weather'][0]['main']
    temp = round(weather_data.json()['main']['temp'])
    temp_min = round(weather_data.json()['main']['temp_min'])
    temp_max = round(weather_data.json()['main']['temp_max'])
    
    print(f'The weather in {user_input} is: {weather}')
    print(f'The temperature in {user_input} is: {temp}')
    print(f'The minimum temperature in {user_input} is: {temp_min}')
    print(f'The maximum temperature in {user_input} is: {temp_max}')

