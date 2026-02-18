"""
Smart Irrigation Advice Chatbot - Main Application
CLI interface for getting irrigation recommendations based on weather and crop type.
"""

import sys
from config import validate_config
from weather_api import get_weather_data, WeatherAPIError
from llm_integration import get_irrigation_recommendation, format_recommendation_output, LLMIntegrationError


def get_user_input():
    """
    Get crop type and location from user input.
    
    Returns:
        tuple: (crop_type, city) or (None, None) if user wants to exit
    """
    print("\n" + "=" * 70)
    print("SMART IRRIGATION ADVICE CHATBOT")
    print("=" * 70)
    print("\nWelcome! I'll help you make informed irrigation decisions based on")
    print("current weather conditions and your crop type.")
    print("\nType 'exit' or 'quit' at any time to exit the program.\n")
    
    # Get crop type
    while True:
        crop_type = input("Enter crop type (e.g., wheat, rice, tomato, corn): ").strip()
        
        if crop_type.lower() in ['exit', 'quit']:
            return None, None
        
        if not crop_type:
            print("⚠️  Crop type cannot be empty. Please try again.")
            continue
        
        if len(crop_type) < 2:
            print("⚠️  Please enter a valid crop type (at least 2 characters).")
            continue
        
        break
    
    # Get city/location
    while True:
        city = input("Enter your city/location (e.g., London, New York, Mumbai): ").strip()
        
        if city.lower() in ['exit', 'quit']:
            return None, None
        
        if not city:
            print("⚠️  City cannot be empty. Please try again.")
            continue
        
        if len(city) < 2:
            print("⚠️  Please enter a valid city name (at least 2 characters).")
            continue
        
        break
    
    return crop_type, city


def main():
    """
    Main function to run the irrigation advice chatbot.
    """
    # Validate configuration
    is_valid, error_message = validate_config()
    if not is_valid:
        print("\n❌ Configuration Error:")
        print(f"   {error_message}")
        print("\n📝 Setup Instructions:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your API keys to the .env file")
        print("   3. Get OpenWeatherMap API key: https://openweathermap.org/api")
        print("   4. Get OpenAI API key: https://platform.openai.com/api-keys")
        sys.exit(1)
    
    try:
        # Main loop to allow multiple recommendations without recursion
        while True:
            # Get user input
            crop_type, city = get_user_input()
            
            if crop_type is None:
                print("\n👋 Thank you for using Smart Irrigation Advice Chatbot. Goodbye!")
                sys.exit(0)
            
            # Fetch weather data
            print(f"\n🌤️  Fetching weather data for {city}...")
            try:
                weather_info = get_weather_data(city)
                print("✅ Weather data retrieved successfully!")
            except WeatherAPIError as e:
                print(f"\n❌ Weather API Error: {str(e)}")
                print("   Please check your city name and try again.")
                # Ask if they want to retry instead of exiting
                retry = input("\nWould you like to try again? (yes/no): ").strip().lower()
                if retry in ['yes', 'y']:
                    continue
                else:
                    sys.exit(1)
            
            # Get irrigation recommendation from LLM
            print(f"🤖 Generating irrigation recommendations for {crop_type}...")
            try:
                recommendation = get_irrigation_recommendation(crop_type, weather_info)
                print("✅ Recommendation generated successfully!\n")
            except LLMIntegrationError as e:
                print(f"\n❌ LLM Integration Error: {str(e)}")
                print("   Please check your OpenAI API key and try again.")
                sys.exit(1)
            
            # Display formatted output
            output = format_recommendation_output(crop_type, weather_info, recommendation)
            print(output)
            
            # Ask if user wants to get another recommendation
            while True:
                another = input("\nWould you like to get another recommendation? (yes/no): ").strip().lower()
                if another in ['yes', 'y']:
                    break  # Break inner loop to continue outer loop
                elif another in ['no', 'n', 'exit', 'quit']:
                    print("\n👋 Thank you for using Smart Irrigation Advice Chatbot. Goodbye!")
                    sys.exit(0)
                else:
                    print("⚠️  Please enter 'yes' or 'no'.")
        
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        print("   Please try again or contact support if the issue persists.")
        sys.exit(1)


if __name__ == "__main__":
    main()
