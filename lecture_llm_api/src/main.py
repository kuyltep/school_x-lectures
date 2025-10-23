import os
from rich import print

from openai import OpenAI, completions

from common.settings import OpenAISettings




def get_client() -> OpenAI:
    settings = OpenAISettings()
    client = OpenAI(
        api_key=settings.openai_api_key.get_secret_value(),
        base_url=str(settings.openai_base_url),
    )
    return client


def responses_variant():
    client = get_client()

    completion = client.responses.create(
        model="Qwen/Qwen3-Next-80B-A3B-Instruct",
        instructions="Ты русский православный батюшка матершинник, который составляет молитвы людям с кучей мата и эмодзи",
        input="Составь молитву, чтобы не ломался автобус от ДГТУ до Шаповалова",
    )

    print(completion.output_text)


messages = [
    {
        "role": "system",
        "content": "Ты русский православный батюшка матершинник, который составляет молитвы людям с кучей мата и брани, и эмодзи",
    },
    {
        "role": "user",
        "content": "/no_think Составь молитву, чтобы не ломался автобус от ДГТУ до Шаповалова",
    },
]


def completions_variant():
    client = OpenAI()
    completion = client.chat.completions.create(
        model="Qwen/Qwen3-Next-80B-A3B-Instruct",
        messages=messages,
    )
    messages.append(
        {
            "role": "assistant",
            "content": completion.choices[0].message.content,
        }
    )
    # ... read task below ...


if __name__ == "__main__":
    # responses_variant()
    completions_variant()
    print(messages)

    # ЗАДАЧА:
    # сделать бесконечй цикл для диалога с моделью в одном чате с сохранением всего этого контекста
    # если пользователь вводит "/exit", то выйти из цикла
    # если вводит "/clear", то очистить историю, кроме system prompt
    # если вводит "/system какой-то текст", то всё что после /system - будет системный промптом
    # для задачи обязательно использовать rich console https://rich.readthedocs.io/en/latest/console.html
    # и panel для красоты https://rich.readthedocs.io/en/latest/panel.html
    # + форматирование через https://rich.readthedocs.io/en/latest/markdown.html
