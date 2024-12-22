# app/config.py

import os
from dotenv import load_dotenv
from pathlib import Path

# Determine the environment
ENV = os.getenv("ENV", "development")  # default to 'development'

# Load the appropriate .env file
if ENV == "testing":
    env_path = Path('.') / '.env.test'
else:
    env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path)

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    WEATHER_API_BASE_URL = os.getenv("WEATHER_API_BASE_URL", "https://api.openweathermap.org/data/2.5/weather")
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

settings = Settings()