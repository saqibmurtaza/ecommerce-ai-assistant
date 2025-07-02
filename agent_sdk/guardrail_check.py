from agents import (Agent, Runner, RunConfig, OpenAIChatCompletionsModel,
                    set_tracing_disabled,ModelSettings)
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

set_tracing_disabled(disabled=True)

BASE_URL= os.getenv('BASE_URL')
API_KEY= os.getenv('API_KEY')
MODEL_NAME= os.getenv('MODEL_NAME')

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError("Check Base url | Api_key | Model Name")

external_client= AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

model= OpenAIChatCompletionsModel(
    model=MODEL_NAME,
    openai_client=external_client
)

config= RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

###############################
# INPUT GUARDRAIL
###############################

from agents import (
    RunContextWrapper, TResponseInputItem,
    input_guardrail, InputGuardrailResult,
    GuardrailFunctionOutput, 
    InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered,
    OutputGuardrailResult
)
from pydantic import BaseModel

# DEFINE PYDANTIC CLASS TO CHECK OUTPUT STRUCTURE FOR INPUT
class InputFormatChecker(BaseModel):
    is_english: bool
    reason: str

guardrail_agent= Agent(
    name="Input_Guardrail_Agent",
    instructions="""
    You are an expert at determining if user input is written in the English language.
    Your response MUST be a JSON object with two fields:
    - `is_english`: a boolean, true if the input is English, false otherwise.
    - `reason`: a string explaining your decision.

    Examples:
    Input: "Hello, how are you?"
    Output: {"is_english": true, "reason": "The sentence is standard English."}

    Input: "Bonjour, comment ça va?"
    Output: {"is_english": false, "reason": "The sentence is French, not English."}

    Input: "Is ko Translate karo"
    Output: {"is_english": false, "reason": "The sentence contains Urdu/Hinglish words and is not fully English."}
    """,
    output_type=InputFormatChecker,
    model=model, # <--- VERY IMPORTANT: Ensure the guardrail_agent knows which LLM to use!
    model_settings= ModelSettings(
        temperature=0
    )
)

# guardrail function runs to produce a GuardrailFunctionOutput,
# which is then wrapped in an InputGuardrailResult

@input_guardrail
async def input_guardrail_function(ctx: RunContextWrapper[None],
                                    agent: Agent,
                                    input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:

    print(f"DEBUG: Input to guardrail_agent: '{input}'") # Add debug print
    try:
        result= await Runner.run(
            agent,
            input,
            context=ctx.context,
            run_config=config,
            max_turns=3
        )

        print(f"DEBUG: Guardrail Agent Raw Output: {result.raw_output}") # Add debug print
        print(f"DEBUG: Guardrail Agent Parsed Output: {result.final_output}") # Add debug print
        print(f"DEBUG: is_english value: {result.final_output.is_english}")
        print(f"DEBUG: Tripwire will be triggered if 'is_english' is false: {not result.final_output.is_english}")
    except MaxTurnsExceeded:
        print("The agent exceeded the maximum number of turns for the overall run.")


    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered= not result.final_output.is_english # <--- This logic is correct!
    )
spanish_agent= Agent(
    name='Sapnish_Agent',
    model=model,
)

french_agent= Agent(
    name="French_Agent",
    model=model,
)

orch_agent= Agent(
    name="Triage_Agent",
    instructions="""
    - You are smart enough to use tools for translations of user_input.
    - Provide input to all available language options you have.
    """,
    tools= [
        spanish_agent.as_tool(
            tool_name="Spanish_Translator",
            tool_description="Translate Text to Sapnish."
        ),
        french_agent.as_tool(
            tool_name="French_Translaor",
            tool_description="Translate Text to French."
        ),
    ],
    input_guardrails=[input_guardrail_function],
)

async def main():
    print(f"Starting point of main function")
    try:
        result= await Runner.run(
            orch_agent,
            'how are you?',
            run_config=config,
            max_turns= 5
        )
        print(result)
    except InputGuardrailTripwireTriggered:
        print("Input is not and english sentence")
    except MaxTurnsExceeded: # <-- Catch this exception as well
        print("The agent exceeded the maximum number of turns for the overall run.")

if __name__ == "__main__":
    import asyncio
    from agents import MaxTurnsExceeded
    asyncio.run(main())