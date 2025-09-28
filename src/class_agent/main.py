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
from dataclasses import dataclass

load_dotenv(find_dotenv())
api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=api_key
    )
set_tracing_disabled(True)

llm_model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="gemini-2.5-flash")

@dataclass
class User:
    name: str
    age: int
    location: str

@function_tool
def user_info(ctx: RunContextWrapper[User]) -> str:
    return f"User {ctx.context.name} is {ctx.context.age} years old and lives in {ctx.context.location}."

def dynamic_instruction(ctx: RunContextWrapper[User], agent:Agent) -> str:
    if ctx.context.age < 18:
        return "You are a minor, i cant Assist you any more."
    else:
        return "You are a helpful assistant, which can use user_info tool to get user informations."
    
user1 = User(name="Khan", age=35, location="Lahore")

agent = Agent[User](
    name="Class Agent",
    instructions=dynamic_instruction,
    model=llm_model,
    tools=[user_info]
)

def main():
    result = Runner.run_sync(
        starting_agent=agent,
        input="what is user current location,age and name",
        context=user1
    )
    print(result.final_output)

if __name__ == "__main__":
    main()
