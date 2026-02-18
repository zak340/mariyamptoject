# API Usage Report

## Overview

This document provides detailed information about the APIs used in the Smart Irrigation Advice Chatbot, including endpoint specifications, parameters, response structures, and LLM prompt design methodology.

## 1. OpenWeatherMap API

### API Details
- **Base URL**: `https://api.openweathermap.org/data/2.5/weather`
- **API Type**: RESTful API
- **Authentication**: API key via query parameter
- **Rate Limits**: Free tier allows 60 calls/minute, 1,000,000 calls/month

### Endpoint Used

**Current Weather Data**
```
GET https://api.openweathermap.org/data/2.5/weather
```

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `q` | string | Yes | City name (e.g., "London" or "London,UK") |
| `appid` | string | Yes | API key for authentication |
| `units` | string | No | Units of measurement (metric, imperial, standard). Default: metric |

### Example Request
```
GET https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY&units=metric
```

### Response Structure

The API returns a JSON object with the following key fields:

```json
{
  "coord": {
    "lon": -0.1257,
    "lat": 51.5085
  },
  "weather": [
    {
      "id": 500,
      "main": "Rain",
      "description": "light rain",
      "icon": "10d"
    }
  ],
  "main": {
    "temp": 15.3,
    "feels_like": 14.8,
    "temp_min": 13.5,
    "temp_max": 17.2,
    "pressure": 1013,
    "humidity": 72
  },
  "wind": {
    "speed": 3.5,
    "deg": 230
  },
  "clouds": {
    "all": 85
  },
  "rain": {
    "1h": 2.3
  },
  "sys": {
    "country": "GB"
  },
  "name": "London"
}
```

### Data Fields Extracted

Our application extracts and uses the following fields:

| Field | Path in JSON | Description | Unit |
|-------|--------------|-------------|------|
| City Name | `name` | Name of the city | String |
| Country | `sys.country` | Country code | String |
| Temperature | `main.temp` | Current temperature | Celsius (°C) |
| Feels Like | `main.feels_like` | Perceived temperature | Celsius (°C) |
| Humidity | `main.humidity` | Humidity percentage | % |
| Weather Condition | `weather[0].main` | Main weather category | String |
| Description | `weather[0].description` | Detailed weather description | String |
| Wind Speed | `wind.speed` | Wind speed | m/s |
| Cloud Coverage | `clouds.all` | Cloud coverage percentage | % |
| Rainfall (1h) | `rain.1h` | Rainfall in last hour | mm |
| Rainfall (3h) | `rain.3h` | Rainfall in last 3 hours | mm |

### Error Handling

| Status Code | Description | Our Handling |
|-------------|-------------|--------------|
| 200 | Success | Process weather data |
| 401 | Invalid API key | Display authentication error |
| 404 | City not found | Prompt user to check city name |
| 429 | Rate limit exceeded | Suggest retry later |
| 500 | Server error | Display API unavailable message |

### Implementation Details

**File**: `weather_api.py`

**Key Functions**:
- `get_weather_data(city)`: Fetches weather data for a given city
- `format_weather_summary(weather_info)`: Formats weather data for display

**Error Handling**: Custom `WeatherAPIError` exception for all API-related errors

## 2. OpenAI GPT API

### API Details
- **API Type**: RESTful API
- **Authentication**: Bearer token (API key in header)
- **Model Used**: gpt-4o-mini (configurable)
- **Rate Limits**: Depends on account tier

### Endpoint Used

**Chat Completions**
```
POST https://api.openai.com/v1/chat/completions
```

### Request Structure

```json
{
  "model": "gpt-4o-mini",
  "messages": [
    {
      "role": "system",
      "content": "You are an agricultural irrigation expert who provides practical, clear advice to farmers."
    },
    {
      "role": "user",
      "content": "[Detailed prompt with crop and weather data]"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 800
}
```

### Parameters Used

| Parameter | Value | Description |
|-----------|-------|-------------|
| `model` | gpt-4o-mini | The LLM model to use |
| `messages` | Array | Conversation history with system and user messages |
| `temperature` | 0.7 | Controls randomness (0-2). 0.7 provides balanced creativity |
| `max_tokens` | 800 | Maximum length of generated response |

### Response Structure

```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "gpt-4o-mini",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "[Irrigation recommendation text]"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 450,
    "completion_tokens": 350,
    "total_tokens": 800
  }
}
```

### Implementation Details

**File**: `llm_integration.py`

**Key Functions**:
- `create_irrigation_prompt(crop_type, weather_info)`: Creates structured prompt
- `get_irrigation_recommendation(crop_type, weather_info)`: Calls OpenAI API
- `format_recommendation_output(crop_type, weather_info, recommendation)`: Formats output

## 3. LLM Prompt Design Methodology

### Design Principles

1. **Role Definition**: Clearly define the AI's role as an "agricultural expert specializing in irrigation management"

2. **Context Provision**: Provide comprehensive context including:
   - Crop type
   - Complete weather data (temperature, humidity, rainfall, wind, clouds)
   - Location information

3. **Structured Output**: Request specific sections to ensure consistent, actionable advice:
   - Irrigation Decision (Yes/No/Consider)
   - Recommended Frequency
   - Duration
   - Best Time
   - Precautions
   - Additional Tips

4. **Audience Consideration**: Explicitly request "beginner-friendly" language and "simple" explanations

5. **Practical Focus**: Emphasize practical, actionable recommendations over theoretical knowledge

### Prompt Template

```
You are an agricultural expert specializing in irrigation management. Based on the current weather conditions and crop type, provide specific irrigation recommendations for a farmer.

Crop Type: {crop_type}

Current Weather Conditions:
- Location: {city}, {country}
- Temperature: {temperature}°C (feels like {feels_like}°C)
- Humidity: {humidity}%
- Weather: {description}
- Wind Speed: {wind_speed} m/s
- Cloud Coverage: {clouds}%
- Recent Rainfall: {rain_1h} mm (last hour) or {rain_3h} mm (last 3 hours)

Please provide irrigation advice in the following format:

1. IRRIGATION DECISION: (Yes/No/Consider) with a brief reason
2. RECOMMENDED FREQUENCY: How often to irrigate (e.g., daily, every 2 days)
3. DURATION: Approximate irrigation duration per session
4. BEST TIME: Best time of day to irrigate
5. PRECAUTIONS: Any weather-based precautions
6. ADDITIONAL TIPS: Crop-specific advice

Keep your response concise, practical, and beginner-friendly. Use simple language that a farmer with basic knowledge can understand.
```

### Prompt Engineering Techniques Used

1. **System Message**: Sets the AI's persona and expertise domain
2. **Structured Input**: Weather data presented in clear, labeled format
3. **Numbered Sections**: Guides the AI to produce organized output
4. **Explicit Constraints**: "Concise", "practical", "beginner-friendly" ensure appropriate tone
5. **Examples in Instructions**: Parenthetical examples help guide output format

### Temperature Setting Rationale

**Temperature: 0.7**
- Balanced between creativity (higher values) and consistency (lower values)
- Allows for natural language variation while maintaining factual accuracy
- Suitable for practical advice that needs some flexibility but must remain grounded in agricultural principles

### Token Limit Rationale

**Max Tokens: 800**
- Sufficient for comprehensive recommendations covering all required sections
- Prevents overly verbose responses
- Allows for detailed explanations while maintaining readability
- Typical response uses 300-500 tokens, leaving buffer for complex scenarios

## 4. Example Use Cases

### Use Case 1: Recent Rainfall

**Input**:
- Crop: Tomato
- Location: London, GB
- Weather: Light rain, 15°C, 72% humidity, 2.3mm rainfall (last hour)

**Expected Output Sections**:
1. Irrigation Decision: "No - Recent rainfall has provided adequate moisture"
2. Frequency: "Monitor soil moisture; likely no irrigation needed for 2-3 days"
3. Duration: "N/A for now"
4. Best Time: "N/A, but when needed, early morning"
5. Precautions: "Check soil drainage, avoid overwatering"
6. Additional Tips: "Tomatoes need consistent moisture but not waterlogged soil"

### Use Case 2: Hot and Dry Conditions

**Input**:
- Crop: Wheat
- Location: Phoenix, AZ
- Weather: Clear sky, 35°C, 25% humidity, no rainfall

**Expected Output Sections**:
1. Irrigation Decision: "Yes - High temperature and low humidity increase water needs"
2. Frequency: "Daily irrigation recommended during this heat wave"
3. Duration: "30-45 minutes per session, depending on system"
4. Best Time: "Early morning (5-7 AM) or late evening (7-9 PM)"
5. Precautions: "Avoid midday irrigation to minimize evaporation"
6. Additional Tips: "Wheat is drought-tolerant but needs water during grain filling stage"

### Use Case 3: Moderate Conditions

**Input**:
- Crop: Rice
- Location: Mumbai, India
- Weather: Partly cloudy, 28°C, 65% humidity, 0.5mm rainfall

**Expected Output Sections**:
1. Irrigation Decision: "Consider - Moderate conditions with light rainfall"
2. Frequency: "Every 2 days if soil moisture is low"
3. Duration: "20-30 minutes"
4. Best Time: "Early morning"
5. Precautions: "Rice needs standing water; maintain 5-10cm water level in field"
6. Additional Tips: "Monitor water level rather than irrigation schedule"

## 5. API Integration Best Practices

### Security
- ✅ API keys stored in environment variables
- ✅ `.env` file excluded from version control
- ✅ `.env.example` provided for setup guidance
- ✅ No hardcoded credentials

### Error Handling
- ✅ Network errors (timeout, connection)
- ✅ Authentication errors
- ✅ Rate limiting
- ✅ Invalid input validation
- ✅ Malformed API responses

### Performance
- ✅ API timeout set to 10 seconds
- ✅ Single API call per recommendation
- ✅ Efficient data parsing
- ✅ Minimal token usage

### User Experience
- ✅ Clear progress indicators
- ✅ Helpful error messages
- ✅ Input validation with feedback
- ✅ Formatted, readable output

## 6. Future Enhancements

Potential improvements for future versions:

1. **Weather API**:
   - Add 5-day forecast for planning
   - Include soil temperature data
   - Add UV index for crop protection

2. **LLM Integration**:
   - Implement conversation history for follow-up questions
   - Add support for multiple crops in same query
   - Include seasonal recommendations

3. **Features**:
   - Irrigation schedule reminders
   - Historical weather tracking
   - Crop disease detection based on weather patterns
   - Multi-language support

4. **Technical**:
   - Caching for repeated city queries
   - Batch processing for multiple fields
   - Web interface (Flask/FastAPI)
   - Database for storing recommendations

## 7. Cost Analysis

### OpenWeatherMap (Free Tier)
- **Limit**: 60 calls/minute, 1,000,000 calls/month
- **Cost**: Free
- **Usage**: 1 call per recommendation
- **Estimate**: Supports unlimited users within rate limits

### OpenAI GPT-4o-mini
- **Pricing** (as of 2024):
  - Input: $0.150 per 1M tokens
  - Output: $0.600 per 1M tokens
- **Usage per request**:
  - Input: ~450 tokens
  - Output: ~350 tokens
- **Cost per request**: ~$0.00028
- **100 requests**: ~$0.028
- **1000 requests**: ~$0.28

**Note**: Actual costs may vary based on OpenAI pricing updates and usage patterns.

## Conclusion

This application demonstrates effective integration of weather data APIs and LLMs to solve real-world agricultural problems. The prompt design methodology ensures consistent, practical, and actionable recommendations while maintaining simplicity for end users.