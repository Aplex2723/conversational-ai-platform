import requests
from loguru import logger
from app.config import settings

def get_weather_for_newyork():
    params = {
        'q': 'New York',
        'appid': settings.WEATHER_API_KEY,
        'units': 'metric',  # or 'imperial'
        'lang': 'en'
    }
    logger.info("Fetching weather data for New York from OpenWeather API.")
    try:
        response = requests.get(settings.WEATHER_API_BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception: {req_err}")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
    return {}