import asyncio
import time
import os

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.utils.log import logger
from agno.tools.duckduckgo import DuckDuckGoTools

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_base_url = os.getenv("OPENAI_API_BASE_URL")
openai_model = os.getenv("OPENAI_MODEL")

async_agent = Agent(
    model=OpenAIChat(
      id=openai_model,
      api_key=openai_api_key,
      base_url=openai_base_url,
      supports_native_structured_outputs=False,
      provider="OpenRouter"
      ),
    stream=True,
    tools=[DuckDuckGoTools()],
    markdown=True,
    instructions="Твоя задача - поиск информации в интернете и возврат акутальной информации на запрос пользователя",
)

asyncio.run(
    async_agent.aprint_response("Как зовут инстасамку?", stream=True)
)