from services.weather_service import WeatherService

def get_current_weather(city_name):
    """
    Queries OpenWeather API for weather data of the given city name.
    Delegates to the centralized WeatherService.
    """
    return WeatherService.get_weather(city_name)
