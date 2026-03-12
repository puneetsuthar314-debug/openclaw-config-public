---
name: weather
description: Get current weather and forecasts via wttr.in or Open-Meteo. Use when user asks about weather, temperature, or forecasts for any location.
---

# Weather Skill

Get weather information using free APIs (no API key needed).

## When to Use

- User asks about current weather
- User wants a forecast
- User asks about temperature, rain, wind
- User is planning outdoor activities

## APIs Used

### wttr.in (Default)
- URL: `https://wttr.in/{location}`
- No API key required
- Supports text and ANSI output

### Open-Meteo (Fallback)
- URL: `https://api.open-meteo.com/v1/forecast`
- No API key required
- JSON output

## Usage Examples

```bash
# Current weather (Shanghai)
curl "wttr.in/Shanghai?format=3"

# Forecast (3 days)
curl "wttr.in/Shanghai?format=3"

# Detailed JSON (Open-Meteo)
curl "https://api.open-meteo.com/v1/forecast?latitude=31.2304&longitude=121.4737&current_weather=true"
```

## Output Format

**Simple:**
```
Shanghai: 🌤️ +22°C, Wind: 15 km/h, Humidity: 65%
```

**Detailed:**
```
📍 Shanghai, China
🌡️  Current: 22°C (Feels like 21°C)
☁️   Condition: Partly cloudy
💨  Wind: 15 km/h NW
💧  Humidity: 65%
🌧️  Precipitation: 10% chance
```

## Common Locations

| Location | Coordinates |
|----------|-------------|
| Shanghai | 31.2304, 121.4737 |
| Beijing | 39.9042, 116.4074 |
| Shenzhen | 22.5431, 114.0579 |
| Hangzhou | 30.2741, 120.1551 |

## Tips

1. Default to Shanghai if location not specified
2. Include emoji for visual clarity
3. Add clothing/activity suggestions based on weather
4. Warn about extreme conditions (heat, cold, rain)
