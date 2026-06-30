import urllib.request
import urllib.parse
import json
from django.conf import settings

def get_current_weather(city_name):
    """
    Queries OpenWeather API for weather data of the given city name.
    Returns a dictionary of parameters if successful, or None on failure.
    """
    api_key = getattr(settings, 'OPENWEATHER_API_KEY', None)
    if not api_key or api_key == 'dummy_api_key':
        return None

    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                return {
                    'temp': round(data['main']['temp']),
                    'condition': data['weather'][0]['main'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed'],
                    'icon': data['weather'][0]['icon']
                }
    except Exception:
        pass
    return None
