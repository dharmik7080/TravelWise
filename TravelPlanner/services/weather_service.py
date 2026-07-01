import urllib.request
import urllib.parse
import json
import logging
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

logger = logging.getLogger(__name__)

class WeatherService:
    """
    Dedicated service for live weather integration using the OpenWeather API.
    Handles caching, timeouts, and error resilience.
    """
    CACHE_TIMEOUT = 1800  # 30 minutes in seconds

    @classmethod
    def get_weather(cls, city_name):
        if not city_name:
            return None

        city_slug = city_name.strip().lower()
        cache_key = f"weather_{city_slug}"
        
        # 1. Read from cache
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        # 2. API Key verification
        api_key = getattr(settings, 'OPENWEATHER_API_KEY', None)
        if not api_key or api_key == 'dummy_api_key':
            logger.warning("OpenWeather API key is not configured or is set to default 'dummy_api_key'.")
            return None

        # 3. Build API request
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city_name,
            'appid': api_key,
            'units': 'metric'
        }
        url = f"{base_url}?{urllib.parse.urlencode(params)}"
        
        # 4. Make request with timeout and exception safety
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'TravelWise/1.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    
                    weather_data = {
                        'temp': round(data['main']['temp']),
                        'condition': data['weather'][0]['main'],
                        'humidity': data['main']['humidity'],
                        'wind_speed': data['wind']['speed'],
                        'icon': data['weather'][0]['icon'],
                        'last_updated': timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    # Store to cache
                    cache.set(cache_key, weather_data, cls.CACHE_TIMEOUT)
                    return weather_data
        except Exception as e:
            logger.error(f"Error fetching live weather for city '{city_name}': {e}")
            
        return None
