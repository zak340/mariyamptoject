"""
Weather API module for OpenWeatherMap integration.
Fetches real-time weather data for irrigation recommendations.
"""

import requests
from config import OPENWEATHER_API_KEY, OPENWEATHER_BASE_URL


class WeatherAPIError(Exception):
    """Custom exception for weather API errors."""
    pass


def get_weather_data(city):
    """
    Fetch current weather data for a given city from OpenWeatherMap API.
    
    Args:
        city (str): Name of the city
        
    Returns:
        dict: Weather data containing temperature, humidity, precipitation, and conditions
        
    Raises:
        WeatherAPIError: If API call fails or returns invalid data
    """
    if not city or not isinstance(city, str):
        raise WeatherAPIError("City name must be a non-empty string")
    
    if not OPENWEATHER_API_KEY:
        raise WeatherAPIError("OpenWeatherMap API key is not configured")
    
    # Prepare API request parameters
    params = {
        'q': city.strip(),
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric'  # Use Celsius for temperature
    }
    
    try:
        # Make API request
        response = requests.get(OPENWEATHER_BASE_URL, params=params, timeout=10)
        
        # Check for HTTP errors
        if response.status_code == 401:
            raise WeatherAPIError("Invalid API key. Please check your OpenWeatherMap API key.")
        elif response.status_code == 404:
            raise WeatherAPIError(f"City '{city}' not found. Please check the city name.")
        elif response.status_code == 429:
            raise WeatherAPIError("API rate limit exceeded. Please try again later.")
        elif response.status_code != 200:
            raise WeatherAPIError(f"API request failed with status code {response.status_code}")
        
        # Parse JSON response
        data = response.json()
        
        # Extract relevant weather information
        weather_info = {
            'city': data.get('name', city),
            'country': data.get('sys', {}).get('country', 'Unknown'),
            'temperature': data.get('main', {}).get('temp'),
            'feels_like': data.get('main', {}).get('feels_like'),
            'humidity': data.get('main', {}).get('humidity'),
            'conditions': data.get('weather', [{}])[0].get('main', 'Unknown'),
            'description': data.get('weather', [{}])[0].get('description', 'Unknown'),
            'wind_speed': data.get('wind', {}).get('speed'),
            'clouds': data.get('clouds', {}).get('all', 0),
        }
        
        # Check for rain data (last 1 hour or 3 hours)
        rain_data = data.get('rain', {})
        weather_info['rain_1h'] = rain_data.get('1h', 0)
        weather_info['rain_3h'] = rain_data.get('3h', 0)
        
        # Validate that we have essential data
        if weather_info['temperature'] is None or weather_info['humidity'] is None:
            raise WeatherAPIError("Incomplete weather data received from API")
        
        return weather_info
        
    except requests.exceptions.Timeout:
        raise WeatherAPIError("Request timed out. Please check your internet connection.")
    except requests.exceptions.ConnectionError:
        raise WeatherAPIError("Connection error. Please check your internet connection.")
    except requests.exceptions.RequestException as e:
        raise WeatherAPIError(f"Request failed: {str(e)}")
    except (KeyError, ValueError) as e:
        raise WeatherAPIError(f"Failed to parse weather data: {str(e)}")


def format_weather_summary(weather_info):
    """
    Format weather data into a human-readable summary.
    
    Args:
        weather_info (dict): Weather data from get_weather_data()
        
    Returns:
        str: Formatted weather summary
    """
    summary = f"Weather in {weather_info['city']}, {weather_info['country']}:\n"
    summary += f"  Temperature: {weather_info['temperature']:.1f}°C (feels like {weather_info['feels_like']:.1f}°C)\n"
    summary += f"  Humidity: {weather_info['humidity']}%\n"
    summary += f"  Conditions: {weather_info['description'].capitalize()}\n"
    summary += f"  Wind Speed: {weather_info['wind_speed']:.1f} m/s\n"
    summary += f"  Cloud Coverage: {weather_info['clouds']}%\n"
    
    if weather_info['rain_1h'] > 0:
        summary += f"  Recent Rainfall: {weather_info['rain_1h']:.1f} mm (last hour)\n"
    elif weather_info['rain_3h'] > 0:
        summary += f"  Recent Rainfall: {weather_info['rain_3h']:.1f} mm (last 3 hours)\n"
    else:
        summary += "  Recent Rainfall: None\n"
    
    return summary
