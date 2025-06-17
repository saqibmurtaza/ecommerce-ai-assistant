import asyncio, os
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner
from agents import Agent, RunConfig, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, set_default_openai_api
from dotenv import load_dotenv
from openai import AsyncOpenAI

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

# async def main():
#     agent = Agent(
#         name="Joker",
#         instructions="You are a helpful assistant.",
#     )

#     result = Runner.run_streamed(
#         agent, input="Please tell me 5 jokes.",
#         run_config=config,
#         )
#     async for event in result.stream_events():
#         if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
#             print(event.data.delta, end="", flush=True)
#             # print(event.data.delta)
#             # print("🚀 Event:", event)


# if __name__ == "__main__":
#     asyncio.run(main())

####################################################
# RunItemStreamEvent dataclass
#####################################################
# import asyncio
# import random
# from agents import Agent, ItemHelpers, Runner, function_tool

# @function_tool
# def how_many_jokes() -> int:
#     return random.randint(1, 10)


# async def main():
#     agent = Agent(
#         name="Joker",
#         instructions="First call the `how_many_jokes` tool, then tell that many jokes.",
#         tools=[how_many_jokes],
#     )

#     result = Runner.run_streamed(
#         agent,
#         input="Hello",
#         run_config=config
#     )
#     print("=== Run starting ===")

#     async for event in result.stream_events():

#         # We'll ignore the raw responses event deltas
#         if event.type == "raw_response_event":
#             continue
#         # When the agent updates, print that
#         elif event.type == "agent_updated_stream_event":
#             print(f"Agent updated: {event.new_agent.name}")
#             continue
#         # When items are generated, print them
#         elif event.type == "run_item_stream_event":
#             if event.item.type == "tool_call_item":
#                 print("-- Tool was called")
#             elif event.item.type == "tool_call_output_item":
#                 print(f"-- Tool output: {event.item.output}")
#             elif event.item.type == "message_output_item":
#                 print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
#             else:
#                 pass  # Ignore other event types
            
#     print("=== Run complete ===")


# if __name__ == "__main__":
#     asyncio.run(main())

########################################################
# Function tools
########################################################
import json

from typing_extensions import TypedDict, Any

from agents import Agent, FunctionTool, RunContextWrapper, function_tool


class Location(TypedDict):
    lat: float
    long: float

@function_tool  
async def fetch_weather(location: Location) -> str:
    
    """Fetch the weather for a given location.

    Args:
        location: The location to fetch the weather for.
    """
    # In real life, we'd fetch the weather from a weather API
    return "sunny"


@function_tool(name_override="fetch_data")  
def read_file(ctx: RunContextWrapper[Any], path: str, directory: str | None = None) -> str:
    """Read the contents of a file.

    Args:
        path: The path to the file to read.
        directory: The directory to read the file from.
    """
    # In real life, we'd read the file from the file system
    return "<file contents>"


agent = Agent(
    name="Assistant",
    tools=[fetch_weather, read_file],  
)

for tool in agent.tools:
    if isinstance(tool, FunctionTool):
        print(tool.name)
        print(tool.description)
        print(json.dumps(tool.params_json_schema, indent=2))
        print()