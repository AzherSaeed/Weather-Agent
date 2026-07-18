import os
import asyncio
import logging

from rich.console import Console
from rich.logging import RichHandler

from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from openai.types.responses import ResponseTextDeltaEvent

from weather import get_weather

console = Console()
load_dotenv(override=True)

AI_MODEL = os.getenv("AI_MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


pre_instruction = """
    you are helpful weather forcast assitent, Give breif detail about weather forcast for specific city

    tools:
    there is additional tool (weather_tool) to get live weather forcast, excute a tool to get updated result

    tasks:
    1 - Verfify live weather forcast result
    2 - create precise message, don't use bullet points
    3 - return response with complete detail of weather forcast
"""


def configure_rich_logging():

    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    handler = RichHandler(
        rich_tracebacks=True,
        markup=True,
        show_path=False,
    )

    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)

    root_logger.addHandler(handler)




async def main():

    configure_rich_logging()

    logger = logging.getLogger(__name__)


    @function_tool
    def weather_tool(city : str):
        logger.info("Weather tool call for live forcast")
        """
        additional to get live weather cast from external sources, provide city name to the get_weather funcation and get complete weather result

        arguments:
        city : specific city name
        """

        result = get_weather(city)

        return result

    agent_1 = Agent(name="get_weather_detail" , instructions=pre_instruction, model=AI_MODEL , tools=[weather_tool])


    


    logger.info("Main file execute for weather")
    result = Runner.run_streamed(agent_1 , input="what is weather of lahore, pakistan")
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data , ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)



if __name__ == "__main__":
    asyncio.run(main())