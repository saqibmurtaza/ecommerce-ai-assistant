# TRACING ENABLED

import asyncio
from agents import Agent, Runner, trace
from openai.types.responses import ResponseTextDeltaEvent
from agent_sdk.tracing_config import init_tracing

print(dir(trace))

model_name = init_tracing()

agent = Agent(
    name="StudyBuddy",
    instructions="You help students learn concepts easily.",
    model=model_name,
)

async def main():
    print("🧪 Starting Agent Streamed Run")

    with trace("study-session"):
        result = Runner.run_streamed(
            agent,
            input="Explain the concept of recursion in programming concisely.",
        )

        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
