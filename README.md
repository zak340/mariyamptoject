# Smart Irrigation Advice Chatbot

A Python-based CLI application that provides intelligent irrigation recommendations by integrating real-time weather data from OpenWeatherMap API with OpenAI GPT's agricultural expertise.

## Overview

This chatbot helps farmers and gardeners make informed irrigation decisions by:
1. Fetching current weather conditions for any location
2. Analyzing weather data in the context of specific crop requirements
3. Providing actionable irrigation recommendations including frequency, duration, timing, and precautions

## Features

- 🌤️ **Real-time Weather Data**: Integrates with OpenWeatherMap API to fetch current weather conditions
- 🤖 **AI-Powered Recommendations**: Uses OpenAI GPT to generate tailored irrigation advice
- 🌾 **Crop-Specific Advice**: Customized recommendations based on crop type
- 💧 **Comprehensive Guidance**: Includes irrigation frequency, duration, timing, and weather-based precautions
- ⚠️ **Error Handling**: Robust error handling for API failures and invalid inputs
- 🔒 **Secure Configuration**: Environment-based API key management

## Project Structure

```
mariyamptoject/
├── main.py                 # CLI application entry point
├── weather_api.py          # OpenWeatherMap API integration
├── llm_integration.py      # OpenAI GPT integration
├── config.py               # Configuration and environment variables
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment file
├── .gitignore             # Git ignore rules
├── README.md              # This file
└── API_USAGE_REPORT.md    # Detailed API usage documentation
```

## Prerequisites

- Python 3.8 or higher
- OpenWeatherMap API key (free tier available)
- OpenAI API key

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/zak340/mariyamptoject.git
   cd mariyamptoject
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   ```
   OPENWEATHER_API_KEY=your_openweathermap_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4o-mini  # Optional, defaults to gpt-4o-mini
   ```

## Getting API Keys

### OpenWeatherMap API Key
1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Navigate to API keys section
4. Copy your API key

### OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up or log in
3. Create a new API key
4. Copy your API key

## Usage

Run the application:
```bash
python main.py
```

Follow the prompts:
1. Enter your crop type (e.g., wheat, rice, tomato, corn)
2. Enter your city/location (e.g., London, New York, Mumbai)
3. Review the irrigation recommendations

### Example Session

```
======================================================================
SMART IRRIGATION ADVICE CHATBOT
======================================================================

Welcome! I'll help you make informed irrigation decisions based on
current weather conditions and your crop type.

Type 'exit' or 'quit' at any time to exit the program.

Enter crop type (e.g., wheat, rice, tomato, corn): tomato
Enter your city/location (e.g., London, New York, Mumbai): London

🌤️  Fetching weather data for London...
✅ Weather data retrieved successfully!
🤖 Generating irrigation recommendations for tomato...
✅ Recommendation generated successfully!

======================================================================
SMART IRRIGATION ADVICE CHATBOT
======================================================================

Crop Type: Tomato
Location: London, GB

----------------------------------------------------------------------
CURRENT WEATHER CONDITIONS
----------------------------------------------------------------------
Temperature: 15.3°C (feels like 14.8°C)
Humidity: 72%
Conditions: Light rain
Wind Speed: 3.5 m/s
Cloud Coverage: 85%
Recent Rainfall: 2.3 mm (last hour)

----------------------------------------------------------------------
IRRIGATION RECOMMENDATION
----------------------------------------------------------------------
[AI-generated recommendations will appear here]

======================================================================
```

## Error Handling

The application handles various error scenarios:
- Invalid or missing API keys
- Invalid city names
- API rate limits
- Network connectivity issues
- Malformed user input

## Security Notes

- ⚠️ Never commit your `.env` file or API keys to version control
- The `.gitignore` file is configured to exclude sensitive files
- Use environment variables for all sensitive configuration

## Technology Stack

- **Language**: Python 3.8+
- **Weather API**: OpenWeatherMap (Current Weather Data API)
- **LLM**: OpenAI GPT (default: gpt-4o-mini)
- **Dependencies**: 
  - `requests` - HTTP requests
  - `openai` - OpenAI API client
  - `python-dotenv` - Environment variable management

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Acknowledgments

- OpenWeatherMap for providing weather data API
- OpenAI for GPT language model
- All contributors to this project
