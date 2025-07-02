import asyncio, os
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner
from agents import Agent, RunConfig, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, set_default_openai_api
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import enable_verbose_stdout_logging

load_dotenv()

set_tracing_disabled(True)

base_url = os.getenv("BASE_URL")
api_key= os.getenv("API_KEY")
model_name = os.getenv("MODEL_NAME")

if not api_key:
    raise ValueError ("Check and update your api_key")

external_client= AsyncOpenAI(
    base_url=base_url,
    api_key=api_key,
)

# set_default_openai_api(external_client)

model= OpenAIChatCompletionsModel(
    model=model_name,
    openai_client=external_client
)

config= RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)


####################################################
# RunItemStreamEvent dataclass
#####################################################
import asyncio
import random
from agents import Agent, ItemHelpers, Runner, function_tool

@function_tool
def how_many_jokes() -> int:
    return random.randint(1, 10)


async def main():
    agent = Agent(
        name="Joker",
        instructions="First call the `how_many_jokes` tool, then tell that many jokes.",
        tools=[how_many_jokes],
    )

    result = Runner.run_streamed(
        agent,
        input="Hello",
        run_config=config
    )
    print("=== Run starting ===")

    async for event in result.stream_events():

        # We'll ignore the raw responses event deltas
        if event.type == "raw_response_event":
            continue
        # When the agent updates, print that
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
            continue
        # When items are generated, print them
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
            else:
                pass  # Ignore other event types
            
    print("=== Run complete ===")
    enable_verbose_stdout_logging()  # <<< enables detailed logs in terminal


if __name__ == "__main__":
    asyncio.run(main())
