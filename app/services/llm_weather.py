from loguru import logger
import openai
from app.config import settings

# Initialize the OpenAI client
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_weather_answer(weather_json: dict):
    if not weather_json:
        logger.warning("No weather data provided.")
        return "I'm sorry, I can't provide the weather details right now."

    try:
        weather_description = weather_json['weather'][0]['description'].capitalize()
        temperature = weather_json['main']['temp']
        feels_like = weather_json['main']['feels_like']
        humidity = weather_json['main']['humidity']
        wind_speed = weather_json['wind']['speed']
        city = weather_json.get('name', 'New York')

        formatted_weather = (
            f"Weather in {city}:\n"
            f"Description: {weather_description}\n"
            f"Temperature: {temperature}°C\n"
            f"Feels Like: {feels_like}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s\n"
        )
        logger.debug(f"Formatted weather data: {formatted_weather}")
    except KeyError as e:
        logger.error(f"Missing key in weather data: {e}")
        return "I'm sorry, I can't parse the weather details right now."

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Summarize this weather data for {city} in a helpful, natural way:\n\n{formatted_weather}"}
    ]
    logger.info("Generating weather summary using LLM.")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        answer = response.choices[0].message.content.strip()
        logger.info("Weather summary generated successfully.")
        return answer
    except Exception as e:
        logger.exception("Weather LLM call failed.")
        return "I'm sorry, I cannot provide the weather details right now."