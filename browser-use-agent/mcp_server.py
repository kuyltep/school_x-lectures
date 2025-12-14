import os
from dotenv import load_dotenv, find_dotenv

from mcp.server.fastmcp import FastMCP


from browser_use import Agent, Browser, ChatOpenAI


load_dotenv(find_dotenv())

api_key = os.getenv("BROWSER_USE_API_KEY")
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
openrouter_base_url = os.getenv("OPENROUTER_API_BASE_URL")
openrouter_model = os.getenv("OPENROUTER_MODEL")


mcp = FastMCP("BrowserUseCloudServer", port=3010)

@mcp.tool()
async def browse_web_cloud(task: str) -> str:
  try:          
    browser = Browser(use_cloud=False)
    llm = ChatOpenAI(
      temperature=0.4,
      reasoning_effort="low",
      api_key=openrouter_api_key,
      base_url=openrouter_base_url,
      model=openrouter_model
    )
    agent = Agent(
        browser=browser,
        task=task,
        llm=llm,
    )
    await agent.run()

  except Exception as e:
      return f"❌ Ошибка выполнения (SDK): {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")