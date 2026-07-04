from weather import get_weather
from translate import translate

OPENAI_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "translate",
            "description": "Translate text into another language.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to translate"
                    },
                    "target_language": {
                        "type": "string",
                        "description": "Target language"
                    }
                },
                "required": [
                    "text",
                    "target_language"
                ]
            }
        }
    }
]

TOOL_REGISTRY = {
    "get_weather": get_weather,
    "translate": translate,
}