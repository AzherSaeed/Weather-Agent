import logging
import requests

logger = logging.getLogger(__name__)

from config import (
    WEATHER_API
)


def get_weather(city: str):
    logger.info("Weather forcast helper calling...")
    try:
        url = (
            f"http://api.weatherapi.com/v1/current.json"
            f"?key={WEATHER_API}&q={city}"
        )

        logger.info(f"Calling Weather API for {city}")
        response = requests.get(url , timeout=10)

        if response.status_code != 200:
            return {
                "error": "Unable to fetch weather."
            }

        data = response.json()

        return {
            "city": data["location"]["name"],
            "country": data["location"]["country"],
            "temperature": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
            "humidity": data["current"]["humidity"],
            "wind": data["current"]["wind_kph"]
        }
    except Exception:
        logger.warning("Weather API does not respond")