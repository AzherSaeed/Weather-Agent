weather_tool = [
    {
        "type" : "function",
        "function" : {
            "name" : "get_weather",
            "description" : "Get current weather for city",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "city" : {
                        "type" : "string",
                        "description" : "city name"
                    }
                },
                "required" : ["city"]
            }
        }
    }
]