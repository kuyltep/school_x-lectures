"""
Default browser-use example using ChatBrowserUse

The simplest way to use browser-use - capable of any web task
with minimal configuration.
"""
import os
import asyncio


from dotenv import load_dotenv

from browser_use import Agent, Browser, ChatBrowserUse

load_dotenv()


openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
openrouter_base_url = os.getenv("OPENROUTER_API_BASE_URL")
openrouter_model = os.getenv("OPENROUTER_MODEL")

async def main():
    browser = Browser(use_cloud=True)
    llm = ChatBrowserUse()
    task = "Найди самый дешевый кастет на Яндекс Маркете"
    agent = Agent(
        browser=browser,
        task=task,
        llm=llm,
    )
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
