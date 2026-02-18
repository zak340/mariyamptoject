"""
LLM integration module for OpenAI GPT.
Generates irrigation recommendations based on crop type and weather data.
"""

from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL


class LLMIntegrationError(Exception):
    """Custom exception for LLM integration errors."""
    pass


def create_irrigation_prompt(crop_type, weather_info):
    """
    Create a detailed prompt for the LLM to generate irrigation recommendations.
    
    Args:
        crop_type (str): Type of crop
        weather_info (dict): Weather data from weather_api module
        
    Returns:
        str: Formatted prompt for the LLM
    """
    prompt = f"""You are an agricultural expert specializing in irrigation management. Based on the current weather conditions and crop type, provide specific irrigation recommendations for a farmer.

Crop Type: {crop_type}

Current Weather Conditions:
- Location: {weather_info['city']}, {weather_info['country']}
- Temperature: {weather_info['temperature']:.1f}°C (feels like {weather_info['feels_like']:.1f}°C)
- Humidity: {weather_info['humidity']}%
- Weather: {weather_info['description']}
- Wind Speed: {weather_info['wind_speed']:.1f} m/s
- Cloud Coverage: {weather_info['clouds']}%
- Recent Rainfall: {weather_info['rain_1h']:.1f} mm (last hour) or {weather_info['rain_3h']:.1f} mm (last 3 hours)

Please provide irrigation advice in the following format:

1. IRRIGATION DECISION: (Yes/No/Consider) with a brief reason
2. RECOMMENDED FREQUENCY: How often to irrigate (e.g., daily, every 2 days)
3. DURATION: Approximate irrigation duration per session
4. BEST TIME: Best time of day to irrigate
5. PRECAUTIONS: Any weather-based precautions
6. ADDITIONAL TIPS: Crop-specific advice

Keep your response concise, practical, and beginner-friendly. Use simple language that a farmer with basic knowledge can understand."""

    return prompt


def get_irrigation_recommendation(crop_type, weather_info):
    """
    Get irrigation recommendations from OpenAI GPT based on crop and weather data.
    
    Args:
        crop_type (str): Type of crop
        weather_info (dict): Weather data from weather_api module
        
    Returns:
        str: LLM-generated irrigation recommendations
        
    Raises:
        LLMIntegrationError: If LLM API call fails
    """
    if not crop_type or not isinstance(crop_type, str):
        raise LLMIntegrationError("Crop type must be a non-empty string")
    
    if not weather_info or not isinstance(weather_info, dict):
        raise LLMIntegrationError("Weather info must be a valid dictionary")
    
    if not OPENAI_API_KEY:
        raise LLMIntegrationError("OpenAI API key is not configured")
    
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Create the prompt
        prompt = create_irrigation_prompt(crop_type, weather_info)
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an agricultural irrigation expert who provides practical, clear advice to farmers."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=800
        )
        
        # Extract the recommendation text
        recommendation = response.choices[0].message.content.strip()
        
        if not recommendation:
            raise LLMIntegrationError("Received empty response from LLM")
        
        return recommendation
        
    except Exception as e:
        # Handle OpenAI-specific errors
        error_msg = str(e)
        if "authentication" in error_msg.lower() or "api_key" in error_msg.lower():
            raise LLMIntegrationError("Invalid OpenAI API key. Please check your API key.")
        elif "rate_limit" in error_msg.lower():
            raise LLMIntegrationError("OpenAI API rate limit exceeded. Please try again later.")
        elif "quota" in error_msg.lower():
            raise LLMIntegrationError("OpenAI API quota exceeded. Please check your account.")
        else:
            raise LLMIntegrationError(f"Failed to get LLM recommendation: {error_msg}")


def format_recommendation_output(crop_type, weather_info, recommendation):
    """
    Format the complete output including weather summary and recommendation.
    
    Args:
        crop_type (str): Type of crop
        weather_info (dict): Weather data
        recommendation (str): LLM-generated recommendation
        
    Returns:
        str: Formatted complete output
    """
    output = "=" * 70 + "\n"
    output += "SMART IRRIGATION ADVICE CHATBOT\n"
    output += "=" * 70 + "\n\n"
    
    output += f"Crop Type: {crop_type.title()}\n"
    output += f"Location: {weather_info['city']}, {weather_info['country']}\n\n"
    
    output += "-" * 70 + "\n"
    output += "CURRENT WEATHER CONDITIONS\n"
    output += "-" * 70 + "\n"
    output += f"Temperature: {weather_info['temperature']:.1f}°C (feels like {weather_info['feels_like']:.1f}°C)\n"
    output += f"Humidity: {weather_info['humidity']}%\n"
    output += f"Conditions: {weather_info['description'].capitalize()}\n"
    output += f"Wind Speed: {weather_info['wind_speed']:.1f} m/s\n"
    output += f"Cloud Coverage: {weather_info['clouds']}%\n"
    
    if weather_info['rain_1h'] > 0:
        output += f"Recent Rainfall: {weather_info['rain_1h']:.1f} mm (last hour)\n"
    elif weather_info['rain_3h'] > 0:
        output += f"Recent Rainfall: {weather_info['rain_3h']:.1f} mm (last 3 hours)\n"
    else:
        output += "Recent Rainfall: None\n"
    
    output += "\n" + "-" * 70 + "\n"
    output += "IRRIGATION RECOMMENDATION\n"
    output += "-" * 70 + "\n"
    output += recommendation + "\n"
    output += "\n" + "=" * 70 + "\n"
    
    return output
