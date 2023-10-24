# def get_weather():
#     import requests
#     api_key = "f5acb50ac7e17eac9343767377447ac4"
#     city = "toshkent"
#     weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&exclude=hourly,daily&appid={api_key}"
#     weather_url = 'https://openweathermap.org/data/2.5/onecall?lat=40.5&lon=68.75&units=metric&appid=439d4b804bc8187953eb36d2a8c26a02'
#     response = requests.get(weather_url)
#     weather_data = response.json()
#     with open('weather.json', 'w') as f:
#         f.write(str(weather_data))
#     return weather_data
# import requests
# import json
from datetime import date
#
# def get_weather(api_key, city):
#     # get 3 Daily weather information
#     daily_weather_url = f"http://api.openweathermap.org/data/2.5/forecast/daily?q={city}&units=metric&cnt=3&appid={api_key}"
#     response = requests.get(daily_weather_url)
#     daily_weather_data = response.json()
#
#
#
#
#     # Soatlik havo ma'lumotlari
#     hourly_weather_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}"
#     response = requests.get(hourly_weather_url)
#     hourly_weather_data = response.json()
#
#     # Bugungi san'at bo'yicha fayl nomi
#     today = date.today()
#     filename = today.strftime("%Y-%m-%d_weather.json")
#
#     # Kunlik va soatlik havo ma'lumotlarini JSON faylga saqlash
#     with open(filename, 'w') as f:
#         json.dump({"daily_weather": daily_weather_data, "hourly_weather": hourly_weather_data}, f)
#
#     return daily_weather_data, hourly_weather_data
#
# # API kaliti va shahar nomi
# api_key = "8bcf303b818a150ee52d4628a4602992"
# city = "Tashkent"
#
# # Kunlik havo va soatlik havo ma'lumotlarini olish
# daily, hourly = get_weather(api_key, city)
#
# print("Kunlik havo ma'lumotlari:")
# print(daily)
#
# print("\nSoatlik havo ma'lumotlari:")
# print(hourly)
import requests
# import time
#
#
# def get_daily_weather(city, api_key, days=3):
#     base_url = "http://api.openweathermap.org/data/2.5/forecast"
#     params = {
#         'q': city,
#         'appid': api_key,
#     }
#
#     response = requests.get(base_url, params=params)
#     weather_data = response.json()
#     if response.status_code == 200:
#         daily_forecast = {}
#         print(weather_data.get('list')[:3])
#         for item in weather_data.get('list'):
#             timestamp = item['dt']
#             date = time.strftime("%Y-%m-%d-%", time.gmtime(timestamp))
#             temp = item['main']['temp']
#             description = item['weather'][0]['description']
#
#             daily_forecast[date] = {
#                 'Temperature (Celsius)': temp - 273.15,
#                 'Description': description,
#             }
#             print(daily_forecast)
#         return daily_forecast
#     else:
#         print(f"Error: {response.status_code}")
#         return None
#
#
# city = "Sirdaryo"
# api_key = "f5acb50ac7e17eac9343767377447ac4"
# days = 3
#
# for day, weather in get_daily_weather(city, api_key, days).items():
#     # print(get_daily_weather(city, api_key, days))
#     print(f"Ob-xavon kun: {day}")
#     print(f"Temperatura (Celsius): {weather['Temperature (Celsius)']:.1f}")
#     print(f"Holat: {weather['Description']}")
#     print()
#

import requests

import requests

def get_three_day_forecast(lat, lon, api_key):
    base_url = f"https://api.openweathermap.org/data/2.5/onecall"
    params = {
        'lat': lat,
        'lon': lon,
        'units': 'metric',
        'exclude': 'current,minutely',
        'appid': api_key,
    }

    response = requests.get(base_url, params=params)
    weather_data = response.json()
    # print(weather_data)
    if response.status_code == 200:
        daily_forecast = weather_data.get('daily')[:7]
        print(type(daily_forecast[0]))
        # for day in daily_forecast:
        #     date = day['dt']
        #     temperature = day['temp']['day']
        #     description = day['weather'][0]['description']
        #     print(f"Ob-xavon kun: {date}")
        #     print(f"Temperatura (Celsius): {temperature:.1f}°C")
        #     print(f"Holat: {description}")
        #     print()
    else:
        print(f"Error: {response.status_code}")

# Quyidagi o'zgaruvchilarni o'zingizga mos ravishda o'zgartiring
lat = 40.5  # Yarim atrofda joylashgan geografik enlem
lon = 68.75  # Yarim atrofda joylashgan geografik boylam
api_key = "f5acb50ac7e17eac9343767377447ac4"  # O'zingizning API kalitingiz

get_three_day_forecast(lat, lon, api_key)
if __name__ == '__main__':
    pass
# import requests
# import json
# import time
#
#
# def get_24_hour_forecast(lat, lon, api_key, output_file):
#     base_url = f"https://api.openweathermap.org/data/2.5/onecall"
#     params = {
#         'lat': lat,
#         'lon': lon,
#         'units': 'metric',
#         'exclude': 'current,minutely,daily',
#         'appid': api_key,
#     }
#
#     response = requests.get(base_url, params=params)
#     weather_data = response.json()
#
#     if response.status_code == 200:
#         hourly_forecast = weather_data.get('hourly')[:24]
#         time1 = weather_data.get('hourly')[:24][0]['dt']
#         time_date = time.strftime("%Y-%m-%d-%H", time.gmtime(time1))
#         current_time = time.strftime("%Y-%m-%d-%H", time.gmtime())
#         print(time_date,current_time)
#
#         with open(output_file, 'w') as file:
#             json.dump(hourly_forecast, file)
#
#         print(f"24 soatlik ob-xavon ma'lumotlari faylga yozildi: {output_file}")
#     else:
#         print(f"Error: {response.status_code}")
#
#
# # Quyidagi o'zgaruvchilarni o'zingizga mos ravishda o'zgartiring
# lat = 40.5  # Yarim atrofda joylashgan geografik enlem
# lon = 68.75  # Yarim atrofda joylashgan geografik boylam
# api_key = "f5acb50ac7e17eac9343767377447ac4"  # O'zingizning API kalitingiz
# output_file = "24_hour_forecast.json"  # Fayl nomi, kutingiz qo'shib o'zgartiring
#
# get_24_hour_forecast(lat, lon, api_key, output_file)
#
# if __name__ == '__main__':
#     pass
