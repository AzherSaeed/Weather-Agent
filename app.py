import sys
import json
import logging

from rich.console import Console
from rich.logging import RichHandler

from llmClient import llm
from TOOLS import OPENAI_TOOLS, TOOL_REGISTRY
from config import configure_logging
from prompts import promptsManager

console = Console()


def configure_rich_logging():
    configure_logging()

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


def main():

    configure_rich_logging()

    logger = logging.getLogger(__name__)

    messages = [
        {
            "role": "system",
            "content": promptsManager.system_prompt_for_weather(),
        }
    ]

    while True:

        question = input("\nYou: ")

        if question.lower() in ["exit", "quit"]:
            break

        messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        logger.info("Sending request to OpenAI")

        response_message = llm.generate(
            messages=messages,
            temperature=1,
            tools=OPENAI_TOOLS,
        )

        if response_message.tool_calls:

            messages.append(response_message)

            for tool_call in response_message.tool_calls:

                tool_name = tool_call.function.name

                arguments = json.loads(
                    tool_call.function.arguments
                )

                logger.info(f"Executing tool: {tool_name}")

                tool_function = TOOL_REGISTRY.get(tool_name)

                if tool_function is None:
                    raise ValueError(
                        f"Unknown tool: {tool_name}"
                    )

                result = tool_function(**arguments)

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result),
                    }
                )

            logger.info("Sending tool result back to OpenAI")

            final_message = llm.generate(
                messages=messages,
                temperature=1,
                tools=None,
            )

            assistant_message = final_message.content

        else:

            assistant_message = response_message.content

        messages.append(
            {
                "role": "assistant",
                "content": assistant_message,
            }
        )

        console.print(
            f"\n[cyan]Assistant:[/cyan] {assistant_message}"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())