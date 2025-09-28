import asyncio
import os
from dotenv import find_dotenv, load_dotenv
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    function_tool,
    RunContextWrapper
)
from agents.result import pretty_print_run_result_streaming   # ✅ use built-in printer
from rich import print
from dataclasses import dataclass

load_dotenv(find_dotenv())
api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=api_key,
)
set_tracing_disabled(True)

llm_model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="gemini-2.5-flash"
)

@dataclass
class User:
    name: str
    age: int
    location: str

@function_tool
def user_info(ctx: RunContextWrapper[User]) -> str:
    return f"User {ctx.context.name} is {ctx.context.age} years old and lives in {ctx.context.location}."

def dynamic_instruction(ctx: RunContextWrapper[User], agent: Agent) -> str:
    if ctx.context.age < 18:
        return "You are a minor. You can't assist about user_info, but you may respond as a helpful assistant for general queries."
    else:
        return "You are a helpful assistant. You can use the user_info tool to get user information."

user1 = User(name="Khan", age=35, location="Lahore")

agent = Agent[User](
    name="Class Agent",
    instructions=dynamic_instruction,
    model=llm_model,
    tools=[user_info]
)

async def mainfun():
    result = Runner.run_streamed(
        starting_agent=agent,
        input="what is capital of pakistan",
        context=user1
    )
    async for event in result.stream_events():
        pretty_print_run_result_streaming(event)  # ✅ Safe printer for your SDK version

def main():
    asyncio.run(mainfun())

if __name__ == "__main__":
    main()
