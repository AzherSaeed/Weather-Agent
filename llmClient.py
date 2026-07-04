from __future__ import annotations



import logging
from typing import Any
from rich.console import Console

from openai import OpenAI
from openai import (
    APIConnectionError,
    APITimeoutError,
    APIStatusError,
    RateLimitError,
)
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from config import (
    AI_MODEL,
    OPENAI_API_KEY,
)

console = Console()
logger = logging.getLogger(__name__)

class OpenAIClient:


    def __init__(self) -> None:
        self.openai = OpenAI(api_key=OPENAI_API_KEY)

    @retry(
        retry=retry_if_exception_type(
            (
                APIConnectionError,
                APITimeoutError,
                RateLimitError,
            )
        ),
        stop=stop_after_attempt(3),
        wait=wait_exponential(
            multiplier=2,
            min=2,
            max=10,
        ),
        reraise=True,
    )

    def generate( self, messages: list[dict[str, Any]], temperature: float = 1.0, tools: list | None = None ):
        kwargs = {}

        if tools is not None:
            kwargs["tools"] = tools

        try:

            response = self.openai.chat.completions.create(
                model=AI_MODEL,
                temperature=temperature,
                messages=messages,
                **kwargs,
            )

            return response.choices[0].message

        except APIStatusError as exc:
            logger.exception("OpenAI API returned an error.")
            raise RuntimeError(
                f"OpenAI API Error ({exc.status_code})"
            )

        except Exception as exc:
            logger.exception("Unexpected LLM error")
            raise RuntimeError(str(exc)) from exc


llm = OpenAIClient()
