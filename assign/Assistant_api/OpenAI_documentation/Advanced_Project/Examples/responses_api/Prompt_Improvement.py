# Import required modules
from openai import AsyncOpenAI
import asyncio
import json
import os
from enum import Enum
from typing import Any, List, Dict
from pydantic import BaseModel, Field
from agents import Agent, Runner, set_default_openai_client, trace

openai_client: AsyncOpenAI | None = None

def _get_openai_client() -> AsyncOpenAI:
    global openai_client
    if openai_client is None:
        openai_client = AsyncOpenAI(
            api_key=os.environ.get("OPENAI_API_KEY", "your-api-key"),
        )
    return openai_client

set_default_openai_client(_get_openai_client())