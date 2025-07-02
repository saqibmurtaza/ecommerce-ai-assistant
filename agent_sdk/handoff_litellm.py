from agents import (Agent, Runner, RunConfig, OpenAIChatCompletionsModel,
                    set_tracing_disabled, handoff)
from openai import AsyncOpenAI
from dotenv import load_dotenv
from agents.extensions.models.litellm_model import LitellmModel
import os

load_dotenv()

set_tracing_disabled(disabled=True)

MODEL_NAME=os.getenv("MODEL_NAME")
print(f"Model name {MODEL_NAME}")
API_KEY=os.getenv("API_KEY")


if not MODEL_NAME:
    raise ValueError("Model Name not found")

model= LitellmModel(
    model=MODEL_NAME,
    api_key=API_KEY
)

#############################################
# Customizing handoffs via the handoff() function
##################################################

from agents import RunContextWrapper
def on_spanish_handoff(ctx: RunContextWrapper[None]):
    print("Handed off to Spanish Agent")

def on_english_handoff(ctx: RunContextWrapper[None]):
    print("Handed off to Spanish Agent")

spanish_agent = Agent(
    name="Spanish Agent",
    instructions="You only speak Spanish and translate to Spanish. Provide ONLY the Spanish translation, nothing else.",
    handoff_description="I am Spanish Speaker.",
    model=model
)

english_agent = Agent(
    name="English agent",
    instructions="You only speak English and translate to English. Provide ONLY the English translation, nothing else.",
    handoff_description="I am english speaker.",
    model=model
)

triage_agent = Agent(
    name="Triage agent",
    instructions="""
    You are a language routing expert for translation requests.
    Your main task is to:
    1.  **Identify the target language** for the translation.
    2.  **Extract the exact text to be translated** from the user's request.
    3.  **Immediately handoff the extracted text to the appropriate 
        specialist agent.**

    **Crucial Rules:**
    -   **Do NOT translate the text yourself.** Your only job is to delegate.
    -   **Do NOT engage in conversation or ask follow-up questions.
        ** Simply perform the handoff or provide the error message.
    -   When handing off, you **MUST provide the extracted text as 
        the input** to the handoff.

    **Handoff Scenarios:**

    **Scenario 1: Translate to Spanish**
    -   If the user asks to translate to Spanish, extract the text they 
        want translated.
    -   Handoff to the 'Spanish agent' with the extracted text as the input.
    -   Example:
        User Input: "Please translate 'How are you?' to Spanish."
        Your Action: Handoff to 'Spanish agent' with input: "How are you?"

        User Input: "Can you convert this sentence to Spanish: 'What is your name?'"
        Your Action: Handoff to 'Spanish agent' with input: "What is your name?"

    **Scenario 2: Translate to English**
    -   If the user asks to translate to English, extract the text they want 
        translated.
    -   Handoff to the 'English agent' with the extracted text as the input.
    -   Example:
        User Input: "Translate 'Bonjour' to English."
        Your Action: Handoff to 'English agent' with input: "Bonjour"

        User Input: "Convert 'नमस्ते' into English."
        Your Action: Handoff to 'English agent' with input: "नमस्ते"

    **Scenario 3: Unsupported Language / Unclear Request**
    -   If the target language is not Spanish or English, or if you cannot 
        clearly determine the text to be translated, you MUST respond with:
        "I can only handle translations to Spanish and English. 
        Please specify one of these languages."
    -   Example:
        User Input: "Translate 'Hello' to German."
        Your Response: "I can only handle translations to Spanish and English. 
        Please specify one of these languages."

        User Input: "Tell me a joke."
        Your Response: "I can only handle translations to Spanish and English. 
        Please specify one of these languages."
    """,
    handoffs= [
        handoff(
            agent=spanish_agent,
            on_handoff=on_spanish_handoff,
            tool_name_override="transfer_to_spanish",
            tool_description_override="Transfer to Spanish-speaking agent."
        ),
        handoff(
            agent=english_agent,
            on_handoff=on_english_handoff,  # Triggered when handed off to French
            tool_name_override="transfer_to_english",
            tool_description_override="Transfer to English-speaking agent"
        )
    ],
    model=model
)


async def main():
    
    try:
        print("\n--- Testing with 'Please translate 'How are you?' to Spanish.' ---")
        result = await Runner.run(
            triage_agent,
            "Please translate 'How are you?' to Spanish.",
            max_turns=5
        )
        print(f"Result (Spanish): {result.final_output}")
        print(f"Last Agent Name : {result.last_agent.name}")

        print("\n--- Testing with 'Convert 'Bonjour' into English.' ---")
        result_english = await Runner.run(
            triage_agent,
            "Convert 'Bonjour' into English.",
            max_turns=5,
        )
        print(f"Result (English): {result_english.final_output}")
        print(f"Last Agent Name : {result_english.last_agent.name}")

        print("\n--- Testing with 'Translate 'Guten Tag' to German.' (Unsupported) ---")
        result_german = await Runner.run(
            triage_agent,
            "Translate 'Guten Tag' to German.",
            max_turns=5
        )
        print(f"Result (German - expected no handoff): {result_german.final_output}")
        print(f"Last Agent Name : {result_german.last_agent.name}")
        
        print("\n--- Testing with 'Tell me something interesting.' (Unclear) ---")
        result_unclear = await Runner.run(
            triage_agent,
            "Tell me something interesting.",
            max_turns=5
        )
        print(f"Result (Unclear - expected no handoff): {result_unclear.final_output}")
        print(f"Last Agent Name : {result_unclear.last_agent.name}")


    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

