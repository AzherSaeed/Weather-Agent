import sys
import json
import logging
from rich.console import Console
from rich.logging import RichHandler


from llmClient import llm
from tools import tools
from weather import get_weather
from config import configure_logging
from prompts import promptsManager




console = Console()


def configure_rich_logging():
    configure_logging()
    

    root_logger = logging.getLogger()

    # Replace default handlers with RichHandler
    root_logger.handlers.clear()

    handler = RichHandler(
        rich_tracebacks=True,
        markup=True,
        show_path=False,
    )


    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)

    root_logger.addHandler(handler)



messages = [
    {
        "role": "system",
        "content": promptsManager.system_prompt_for_weather(),
    }
]

question = input("Type Question: ")

messages.append(
    {
        "role": "user",
        "content": question,
    }
)

    
def main():
    configure_rich_logging()
    logger = logging.getLogger(__name__)
    
    try:

        logger.info("Sending request to OpenAI")
        response_message  = llm.generate(
            messages=messages,
            temperature=1,
            tools=tools
        )

        # if response_message.tool_calls:
        if not isinstance(response_message, str) and response_message.tool_calls:
            tool_call = response_message.tool_calls[0]
            arguments = json.loads(
                tool_call.function.arguments
            )
            city_name = arguments["city"]
            weather_response = get_weather(city_name)
            messages.append(response_message)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(weather_response)
                }
            )
            
            print(weather_response , "weather_responseweather_responseweather_response")

        logger.info("Sending tool result back to OpenAI")
        assistant_message  = llm.generate(
            messages=messages,
            temperature=1,
            tools=None
        )
        logger.info("Assistant respose added in messages")
        messages.append(
            {
                "role": "assistant",
                "content": assistant_message
            }
        )


        console.print(
            f"[cyan]Open AI Response:[/cyan] {assistant_message}"
        )
        return 0

    except KeyboardInterrupt:
        logger.warning("Interrupted by user.")
        return 1

    except Exception:
        logger.exception("Unexpected Application Error")
        return 1

if __name__ == "__main__":
    sys.exit(main())