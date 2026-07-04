from __future__ import annotations

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

####################################################
# Load Environment Variables
####################################################

load_dotenv(override=True)

####################################################
# OpenAI
####################################################

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY is missing from the .env file."
    )

AI_MODEL = os.getenv(
    "AI_MODEL",
    "gpt-5",
)

####################################################
# Tokenizer
####################################################

TOKEN_ENCODING = os.getenv(
    "TOKEN_ENCODING",
    "o200k_base",
)

####################################################
# Chunking
####################################################

MAX_CHUNK_TOKENS = int(
    os.getenv(
        "MAX_CHUNK_TOKENS",
        "2500",
    )
)

CHUNK_OVERLAP = int(
    os.getenv(
        "CHUNK_OVERLAP",
        "250",
    )
)


####################################################
# Temperatures
####################################################

CHUNK_SUMMARIZE_TEMPERATURE = float(
    os.getenv(
        "CHUNK_SUMMARIZE_TEMPERATURE",
        "1",
    )
)

MEETING_ANALYSIS_TEMPERATURE = float(
    os.getenv(
        "MEETING_ANALYSIS_TEMPERATURE",
        "1",
    )
)

####################################################
# Logging
####################################################

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
).upper()


####################################################
# Weather API
####################################################


WEATHER_API = os.getenv("WEATHER_API_KEY")


def configure_logging() -> None:
    """
    Configure application logging.
    """

    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


