"""
Configuration module for Smart Irrigation Advice Chatbot.
Manages environment variables and API keys.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenWeatherMap API Configuration
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
OPENWEATHER_BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

def validate_config():
    """
    Validate that all required configuration values are set.
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not OPENWEATHER_API_KEY:
        return False, "OPENWEATHER_API_KEY is not set. Please add it to your .env file."
    
    if not OPENAI_API_KEY:
        return False, "OPENAI_API_KEY is not set. Please add it to your .env file."
    
    return True, None
