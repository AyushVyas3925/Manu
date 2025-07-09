# G# tasks/weather.py

import requests

def get_weather(city="Delhi", api_key="your weather api key"):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            return f"Error: {data.get('message', 'Unable to fetch weather')}"

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]

        return (
            f"Weather in {city}:\n"
            f"Temperature: {temp}°C\n"
            f"Condition: {desc}\n"
            f"Humidity: {humidity}%"
        )
    except Exception as e:
        return f"Failed to get weather: {e}"
