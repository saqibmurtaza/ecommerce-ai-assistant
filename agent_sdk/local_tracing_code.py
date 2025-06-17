# ✅ Enable Local Tracing + Use Responses API with OpenAI Agent SDK

from agents import (Agent, Runner, trace, 
                    set_default_openai_api, 
                    set_default_openai_client, 
                    set_trace_processors)
from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner
from dotenv import load_dotenv
import asyncio, os

load_dotenv()

base_url = os.getenv("BASE_URL")
api_key= os.getenv("API_KEY")
model_name = os.getenv("MODEL_NAME")

if not base_url or not api_key or not model_name:
    raise ValueError("Please set BASE_URL, GEMINI_API_KEY, MODEL_NAME via env var or code.")

external_client= AsyncOpenAI(
    base_url=base_url,
    api_key=api_key
)

# Configure the external-client
set_default_openai_client(client=external_client, use_for_tracing=True)
set_default_openai_api("chat_completions")

# 👤 Define your agent
agent = Agent(
    name="StudyBuddy",
    instructions="You are a helpful assistant preparing students for exams.",
    # model=model_name,
)

# 🧪 Run an agent using Responses API
async def main():
    print("🚀 Starting agent run with Responses API")

    # 👇 Use Responses API (via Runner.run_streamed)
    result = Runner.run_streamed(
        agent,
        input="What is the difference between JSON schema and Pydantic?"
    )

    async for event in result.stream_events():
        # Filter only delta tokens (text being streamed)
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
