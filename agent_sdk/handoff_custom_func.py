from agents import Agent, Runner, handoff, RunContextWrapper, HandoffInputData
from agents.extensions import handoff_filters
from agents.extensions.models.litellm_model import LitellmModel
from pydantic import BaseModel
from dotenv import load_dotenv
from dataclasses import replace
import os
import asyncio

load_dotenv()

API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

if not MODEL_NAME or not API_KEY:
    raise ValueError("Model Name or Api key not found")

model = LitellmModel(model=MODEL_NAME, api_key=API_KEY)

class QueryData(BaseModel):
    language: str
    query_text: str

spanish_agent = Agent(name="Spanish Agent", model=model)
french_agent = Agent(name="French Agent", model=model)

# Generic on_handoff function
async def custom_on_handoff(
        agent: Agent, 
        ctx: RunContextWrapper[None], 
        input_data: QueryData = None
        ):
    print(f"Handed_off to {agent.name}")
    print(f"Context : {ctx.context}")
    if input_data:
        print(f"Received query: {input_data.query_text}, Language: {input_data.language}")

# Custom input filter
def custom_input_filter(input_data: HandoffInputData) -> HandoffInputData:
    history = input_data.input_history
    print(f"INPUT HISTORY: {history}")
    filtered_history = history[-1:] if isinstance(history, tuple) else history
    return replace(input_data, input_history=filtered_history)

async def on_spanish_handoff(ctx: RunContextWrapper[None], input_data: QueryData):
    print(f"Spanish Agent received query: {input_data.query_text}")
    print(f"Spanish Agent received language: {input_data.language}")

async def on_french_handoff(ctx: RunContextWrapper[None], input_data: QueryData):
    print(f"French Agent received query: {input_data.query_text}")
    print(f"French Agent received language: {input_data.language}")

def custom_input_filter(input_data: HandoffInputData) -> HandoffInputData:
    history = input_data.input_history
    print(f"INPUT HISTORY: {history}")
    filtered_history = history[-1:] if isinstance(history, tuple) else history
    return replace(input_data, input_history=filtered_history)

triage_agent = Agent(
    name="Triage Agent",
    handoffs=[
        handoff(
            agent=spanish_agent,
            on_handoff=lambda ctx, input_data: custom_on_handoff(spanish_agent, ctx, input_data),
            input_type=QueryData,
            input_filter=custom_input_filter,
            tool_name_override="transfer_to_spanish",
            tool_description_override="Transfer to Spanish-speaking agent"
        ),
        handoff(
            agent=french_agent,
            on_handoff=on_french_handoff,
            input_type=QueryData,
            input_filter=handoff_filters.remove_all_tools,
            tool_name_override="transfer_to_french",
            tool_description_override="Transfer to French-speaking agent"
        ),
    ],
    model=model
)

async def main():
    try:
        result_french = await Runner.run(
            triage_agent,
            "Translate to french 'Hello'"
        )
        print(result_french.final_output)
        print(result_french.last_agent.name)

        result_spanish = await Runner.run(
            triage_agent,
            "Translate to spanish 'Hello'"
        )
        print(result_spanish.final_output)
        print(result_spanish.last_agent.name)



    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())