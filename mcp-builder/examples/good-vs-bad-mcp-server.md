# MCP Builder Examples: Good vs Bad Implementations

## 1. Stdio Server and Logging Hygiene

### Bad (Polluted Stdout, Missing Schemas, and Leaked Secrets)

```python
# BAD: Prints debugging info to stdout, polluting the MCP protocol stream
import sys
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather-service")

@mcp.tool()
def get_weather(location: str):
    print(f"DEBUG: fetching weather for {location}")  # Breaks JSON-RPC on stdout!
    api_key = "sk_live_secret12345"
    return f"Weather for {location} using key {api_key}"
```

Defects:
- Prints non-JSON-RPC debug text to `stdout`, corrupting stdio transport and causing client disconnects.
- Embeds hardcoded secret keys.
- Lacks input bounds or parameter descriptions.

### Good (Clean Stderr Logging, Pydantic Schema, and Error Isolation)

```python
# GOOD: Clean stdout JSON-RPC, structured logging to stderr, strict schema
import sys
import logging
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger("weather-service")

mcp = FastMCP("weather-service")

class WeatherInput(BaseModel):
    city: str = Field(..., description="Target city name (e.g. 'London', 'Nairobi')", min_length=2, max_length=100)
    units: str = Field("celsius", description="Temperature unit ('celsius' or 'fahrenheit')")

@mcp.tool(
    name="weather_get_forecast",
    description="Retrieve current weather conditions and 3-day forecast for a specified city."
)
async def get_forecast(params: WeatherInput) -> str:
    logger.info(f"Processing forecast query for city: {params.city}")
    # Implementation logic using environment credentials
    return f"Current temperature in {params.city}: 21 degrees {params.units}."
```

Advantages:
- All diagnostic logs route strictly to `sys.stderr`.
- Strict Pydantic input model generates clean tool JSON schemas.
- Named following `<service>_<verb>_<resource>` convention.
