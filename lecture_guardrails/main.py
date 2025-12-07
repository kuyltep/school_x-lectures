import os
import random
from typing import Callable, Dict, Optional, List
from pydantic import BaseModel, Field
from openai import Client

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langchain.tools import tool
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper

from guardrails import Guard
from guardrails.validators import (
    FailResult,
    PassResult,
    register_validator,
    ValidationResult,
    Validator,
)

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(filename=".env"))

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_base_url = os.getenv("OPENAI_API_BASE_URL")
openai_model = os.getenv("OPENAI_MODEL")
openai_validation_model = os.getenv("OPENAI_VALIDATION_MODEL")

search_wrapper = DuckDuckGoSearchAPIWrapper(max_results=5)

stop_words = ["война", "убийство", "терроризм", "взлом", "наркотики", "порнография",
    "экстремизм", "самоубийство", "насилие", "мошенничество", "кибератака",
    "хакер", "взрыв", "похищение", "преступность", "шпионаж", "коррупция"]


@register_validator(name="stop-words", data_type="string")
class StopWords(Validator):
    def __init__(self, search_words: List[str], on_fail: Optional[Callable] = None):
        super().__init__(on_fail=on_fail, search_words=search_words)
        self.search_words = search_words

    def _validate(self, value: List[str], metadata: Dict) -> ValidationResult:
        mentioned_words = []
        for word in self.search_words:
            if word in value:
                mentioned_words.append(word)

        if len(mentioned_words) > 0:
            return FailResult(
                error_message=f"Запрешенные слова: {', '.join(mentioned_words)}",
            )
        else:
            return PassResult()


@register_validator(name="toxic-message", data_type="string")
class ToxicMessage(Validator):
    validation_prompt = """
    /no_think
    Ты - Ассистент, который занимается оценкой токсичности и негативности сообщений
    Твоя задача анализировать сообщения, которые приходят тебе на вход - это могут быть разные сообщения
    И валидировать их по шкале от 0 до 100 - это оценка токсичности/негативности нашего сообщения
    0 - это значит, что сообщение абсолютно нетоксичное
    100 означает, что сообщение токсичное, негативное и максимально ужасное
    
    Если ассистент отвечает, что он не может помочь в этом вопросе, то мы считаем, что это сообщение с оценкой 0, так как в нем нет токсичнсти
    В ответе верни только число - оценку и больше ничего
    """

    def __init__(self, threshold=70, on_fail: Optional[Callable] = None):
        super().__init__(on_fail=on_fail, threshold=threshold)
        self._threshold = threshold

    def _llm_call(self, messages: list[dict]) -> int:
        openai_client = Client(
            api_key=openai_api_key,
            base_url=openai_base_url,
        )

        response = openai_client.chat.completions.create(
            messages=messages,
            model=openai_validation_model,
            temperature=0.15,
        )

        return int(response.choices[0].message.content)

    def _validate(self, value: str, metadata: Dict) -> ValidationResult:
        messages = [
            {"role": "system", "content": self.validation_prompt},
            {"role": "user", "content": value},
        ]

        score = self._llm_call(messages)

        print(score)
        if score >= self._threshold:
            return FailResult(
                error_message=f"Токсичность сообщения выше {self._threshold}",
            )
        else:
            return PassResult()


guard: Guard = Guard().use_many(StopWords(search_words=stop_words), ToxicMessage(threshold=50))


class GeneratePromoInput(BaseModel):
    sale: int = Field(
        description="Размер скидки по промокоду от 3 до 8 процентов", ge=3, le=8
    )


class GeneratedPromoResponse(GeneratePromoInput):
    def __init_subclass__(cls, **kwargs):
        return super().__init_subclass__(**kwargs)

    promo: str = Field(description="Промокод, состоящий из несокльких символов")


def get_promo_code(num_chars):
    code_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    code = ""
    for i in range(0, num_chars):
        slice_start = random.randint(0, len(code_chars) - 1)
        code += code_chars[slice_start : slice_start + 1]
    return code


def call_tools(last_message) -> list:
    messages = []
    if last_message.tool_calls:
        for tool in last_message.tool_calls:
            print(f"Вызов инструмента: {tool['name']}")
            print(f"Аргументы: {tool['args']}")
            tool_to_call = tools_map[tool["name"]]
            data = tool_to_call(**tool["args"])
            print(data)
            messages.append(data)

    return messages


@tool(
    description="Поиск информации в интернете, если есть пользователь просит найти актуальную информацию на конкретную дату, если просит поискать в интернете, посмотреть новости, поискать информацию"
)
def search(query: str) -> str:
    """Поиск информации в интернете, если есть пользователь просит найти актуальную информацию на конкретную дату, если просит поискать в интернете, посмотреть новости, поискать информацию"""
    return search_wrapper.run(query)


@tool(
    description="Генерация промокода для скидки, если клиент сомневается в выборе нашего сервиса или не уверен в выборе",
    args_schema=GeneratePromoInput,
)
def generate_promocode(sale: int) -> str:
    """Генерация промокода для скидки, если клиент сомневается в выборе нашего сервиса или не уверен в выборе"""
    promo = generate_promocode(6)
    return GeneratedPromoResponse(sale=sale, promo=promo).model_dump_json()


tools = [search, generate_promocode]

tools_map = {"search": search, "generate_promocode": generate_promocode}

checkpointer = InMemorySaver()



SYSTEM_PROMPT = """
Ты — Travel.AI, вежливый и компетентный помощник по путешествиям от компании travel.ai. Твоя задача — помогать пользователям планировать, бронировать и организовывать поездки.
Давайте чёткие, краткие и полезные рекомендации по направлениям, перелётам, проживанию, достопримечательностям, советам путешественникам, визовым требованиям и составлению маршрутов.
Всегда учитывайте безопасность пользователя, его бюджет и предпочтения.

Важные правила поведения:
  Никогда не проявляйте агрессию, не используйте грубость или оскорбления.
  Всегда сохраняйте формальный, уважительный и дружелюбный тон.
  Не обсуждайте нелегальные, запрещённые или этически сомнительные темы.
  Если вопрос пользователя не связан с путешествиями и это не приветственные/прощальные сообщения и вопросы на уточнения деталей, просто ответьте: «К сожалению, я не могу помочь с этим вопросом» — и ничего больше не добавляйте.

Всегда оставайтесь в рамках своей функции помощника по туризму. Если вы не знаете точного ответа — честно скажите об этом, но не пытайтесь угадывать или выдумывать информацию.
"""


class Context(BaseModel):
    user_id: str


model = ChatOpenAI(
    api_key=openai_api_key,
    base_url=str(openai_base_url),
    model=openai_model,
    max_completion_tokens=4096,
    streaming=False,
    # disable_streaming="tool_calling",
    timeout=20,
    temperature=0.3,
)

# model.bind_tools([search, generate_promocode])


agent = create_agent(
    model=model,
    name="Travel.AI Агент",
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
    # tools=tools,
)

config = {"configurable": {"thread_id": "1"}}

context = Context(user_id="1")

while True:
    try:
      user_input = input("Введите запрос для Travel.AI агента: ").strip()
      
      if "exit" in user_input:
        print("Пока")
        break
      
      guard.validate(user_input)

      messages = {"messages": [{"role": "user", "content": user_input}]}

      response = agent.invoke(messages, context=context, config=config)

      last_message = response["messages"][-1]
      print(last_message.content)


      guard.validate(last_message.content)
      # if last_message.tool_calls:
      #     tools_messages = call_tools(last_message)

      #     print(f"Ответ: {last_message.content}")
      # else:
      print(f"Ответ: {last_message.content}")
    except Exception as e:
      print(e)
