import os

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.models.response import ModelResponse
from agno.models.message import Message
from agno.os import AgentOS
from agno.run.agent import RunInput, RunOutput
from agno.exceptions import CheckTrigger, InputCheckError, OutputCheckError
from agno.guardrails import (
    PromptInjectionGuardrail,
    PIIDetectionGuardrail,
    BaseGuardrail,
)

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_base_url = os.getenv("OPENAI_API_BASE_URL")
openai_model = os.getenv("OPENAI_MODEL")
openai_validation_model = os.getenv("OPENAI_VALIDATION_MODEL")

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

VALIDATION_SYSTEM_PROMPT = """
/no_think
Ты - Ассистент, который занимается оценкой токсичности и негативности сообщений
Твоя задача анализировать сообщения, которые приходят тебе на вход - это могут быть разные сообщения
И валидировать их по шкале от 0 до 100 - это оценка токсичности/негативности нашего сообщения
0 - это значит, что сообщение абсолютно нетоксичное
100 означает, что сообщение токсичное, негативное и максимально ужасное

Если ассистент отвечает, что он не может помочь в этом вопросе, то мы считаем, что это сообщение с оценкой 0, так как в нем нет токсичнсти
В ответе верни только число - оценку и больше ничего
"""

STOP_WORDS = [
    "война",
    "убийство",
    "терроризм",
    "взлом",
    "наркотики",
    "порнография",
    "экстремизм",
    "самоубийство",
    "насилие",
    "мошенничество",
    "кибератака",
    "хакер",
    "взрыв",
    "похищение",
    "преступность",
    "шпионаж",
    "коррупция",
]


class StopWordsGuardRail(BaseGuardrail):
    def __init__(self, stop_words: list[str]):
        self.stop_words = stop_words

    def check(self, run_input: RunInput) -> None:
        if isinstance(run_input.input_content, str):
            content = run_input.input_content.lower()
            for word in self.stop_words:
                if word.lower() in content:
                    raise InputCheckError(
                        message=f"Input contains stop word: {word}",
                        check_trigger=CheckTrigger.INPUT_NOT_ALLOWED,
                    )

    def post_check(self, run_output: RunOutput) -> None:
        if isinstance(run_output.content, str):
            content = run_output.content.lower()
            for word in self.stop_words:
                if word.lower() in content:
                    raise OutputCheckError(
                        message=f"Output contains stop word: {word}",
                        check_trigger=CheckTrigger.OUTPUT_NOT_ALLOWED,
                    )


class ToxicDetectionGuardRail(BaseGuardrail):
    def _init_model(self):
        return OpenRouter(
            id=openai_validation_model,
            api_key=openai_api_key,
            base_url=openai_base_url,
            temperature=0.15,
            max_completion_tokens=512,
        )

    def check(self, run_input: RunInput) -> None:
        if isinstance(run_input.input_content, str):
            model = self._init_model()
            messages = [
                Message(role="system", content=VALIDATION_SYSTEM_PROMPT),
                Message(role="user", content=run_input.input_content),
            ]
            response: ModelResponse = model.response(messages)

            if response.content:
                try:
                    score = int(response.content.strip())
                    print(f"Toxic score: {score}")
                    if score > 50:
                        raise InputCheckError(
                            message=f"Too toxic input validation, toxic score: {score}",
                            check_trigger=CheckTrigger.VALIDATION_FAILED,
                        )
                except ValueError:
                    print(f"Invalid toxic score returned: {response.content}")

    async def async_check(self, run_input: RunInput) -> None:
        if isinstance(run_input.input_content, str):
            model = self._init_model()
            messages = [
                Message(role="system", content=VALIDATION_SYSTEM_PROMPT),
                Message(role="user", content=run_input.input_content),
            ]
            response: ModelResponse = await model.aresponse(messages)

            if response.content:
                try:
                    score = int(response.content.strip())
                    print(f"Toxic score: {score}")
                    if score > 50:
                        raise InputCheckError(
                            message=f"Too toxic input validation, toxic score: {score}",
                            check_trigger=CheckTrigger.VALIDATION_FAILED,
                        )
                except ValueError:
                    print(f"Invalid toxic score returned: {response.content}")


stop_words_guardrail = StopWordsGuardRail(stop_words=STOP_WORDS)

agno_agent = Agent(
    name="Agno Agent",
    model=OpenRouter(
        id=openai_model,
        api_key=openai_api_key,
        base_url=openai_base_url,
        temperature=0.4,
        max_completion_tokens=1024,
    ),
    add_history_to_context=False,
    markdown=True,
    instructions=SYSTEM_PROMPT,
    pre_hooks=[
        PromptInjectionGuardrail(),
        PIIDetectionGuardrail(),
        ToxicDetectionGuardRail(),
        stop_words_guardrail,
    ],
    post_hooks=[stop_words_guardrail.post_check],
)

while True:
    try:
        user_input = input("Input your request to Travel.AI agent: ")

        if not user_input or "exit" in user_input.lower():
            print("Bye bye")
            break

        response = agno_agent.run(input=user_input)
        print(response.content)
    except Exception as e:
        print(e)
