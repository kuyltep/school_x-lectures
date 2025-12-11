from agno.agent import Agent
from agno.models.openai import OpenAILike
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(dotenv_path=find_dotenv())

model: OpenAILike = OpenAILike(
    id="Qwen/Qwen3-Next-80B-A3B-Instruct",
    name="Foundation Model",
    provider="cloud.ru",
    supports_native_structured_outputs=True,
    base_url=os.environ.get("OPENAI_BASE_URL"),
    api_key=os.environ.get("OPENAI_API_KEY"),
)

agent: Agent = Agent(
    model=model,
    name="Олег",
    tools=[
        DuckDuckGoTools(
            enable_news=False, fixed_max_results=10, modifier="site:tbank.ru"
        )
    ],
    instructions="Ты работник отдела продаж в крупном Российском банке (Т-Банк), твоя задача - продавать банковские продукты клиентам, которые обращаются к тебе",
    markdown=True,
    stream=True,
)

agent.print_response(
    "Привет, ищу куда и насколкьо положить деньги под проценты, что посоветуешь?"
)
