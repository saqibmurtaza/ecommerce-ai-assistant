import random
from agents import Agent, Runner, function_tool, set_tracing_disabled, OpenAIChatCompletionsModel, RunConfig
from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
from agents import Agent, ItemHelpers, Runner, function_tool
import asyncio, os

load_dotenv()

set_tracing_disabled(disabled=True) # Open AI Tracing == Disable

base_url = os.getenv("BASE_URL")
api_key= os.getenv("API_KEY")
model_name = os.getenv("MODEL_NAME")

if not api_key:
    raise ValueError ("Check and update your api_key")

external_client= AsyncOpenAI(
    base_url=base_url,
    api_key=api_key,
)

model= OpenAIChatCompletionsModel(
    model=model_name,
    openai_client=external_client
)

config= RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)


@function_tool
async def number_of_jokes() -> int:
    """
    Returns the number of jokes to be told.
    """
    result= random.randint(1, 10)
    print(f"Number of jokes to be told: {result}")
    return result

# async def main():
    # agent= Agent(
    #     name="Joker",
    #     instructions="You are a funny assistant. First call the `number_of_jokes` tool, then tell that many jokes.",
    #     tools=[number_of_jokes] 
    # )

    
    # result= Runner.run_streamed(
    #     agent,
    #     "Hello",
    #     run_config=config,
    # )

    
#     async for event in result.stream_events():

#         if event.type == "raw_response_event":
#             # Print model name if present in the event
#             if hasattr(event, "data") and hasattr(event.data, "response") and hasattr(event.data.response, "model"):
#                 print("Model used in this run:", event.data.response.model)
#                 continue
#         # When the agent updates, print that
#         elif event.type == "agent_updated_stream_event":
#             print(f"Agent Name: {event.new_agent.name}")
#             continue
#         # When items are generated, print them
#         elif event.type == "run_item_stream_event":
#             run_item_type = event.item.type  # Get the RunItem type
#             print(f"RunItem type: {run_item_type}")
            
#             if event.item.type == "tool_call_item":
#                 tool_name = event.item.raw_item.name
#                 print(f"-- Tool was called: {tool_name}")
#             elif event.item.type == "tool_call_output_item":
#                 print(f"-- Tool output: {event.item.output}")
#             elif event.item.type == "message_output_item":
#                 print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
#             else:
#                 pass  # Ignore other event types

# if __name__ == "__main__":
#     asyncio.run(main())

# agent = Agent(
#     instructions="You are a helpful assistant."
# )

# ruesult = Runner.run_sync(
#     agent,
#     "Tell me a joke.",
#     run_config=config,
# )
# print(ruesult.final_output)

