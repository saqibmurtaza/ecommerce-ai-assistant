from agents import (Agent, Runner, RunConfig, OpenAIChatCompletionsModel,
                    set_tracing_disabled)
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os, requests, json

load_dotenv()

BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = "mistralai/mistral-small-3.2-24b-instruct-2506:free"



set_tracing_disabled(disabled=True)


external_cleint= AsyncOpenAI(
    base_url=BASE_URL,
    api_key=OPENROUTER_API_KEY
)

model= OpenAIChatCompletionsModel(
    model=MODEL_NAME,
    openai_client=external_cleint
)

config= RunConfig(
    model=model,
    model_provider=external_cleint,
    tracing_disabled=True
)


spanish_agent = Agent(
    name="Spanish Agent",
    instructions="You only speak Spanish and translate to Spanish. Provide ONLY the Spanish translation, nothing else.",
    # model=model
)

english_agent = Agent(
    name="English agent",
    instructions="You only speak English and translate to English. Provide ONLY the English translation, nothing else.",
    # model=model
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
    handoffs=[spanish_agent, english_agent],
    # model=model
)

async def main():
    
    try:
        print("\n--- Testing with 'Please translate 'How are you?' to Spanish.' ---")
        result = await Runner.run(
            triage_agent,
            "Please translate 'How are you?' to Spanish.",
            run_config=config,
            max_turns=5
        )
        print(f"Result (Spanish): {result.final_output}")
        print(f"Last Agent Name : {result.last_agent.name}")

        print("\n--- Testing with 'Convert 'Bonjour' into English.' ---")
        result_english = await Runner.run(
            triage_agent,
            "Convert 'Bonjour' into English.",
            run_config=config,
            max_turns=5
        )
        print(f"Result (English): {result_english.final_output}")
        print(f"Last Agent Name : {result.last_agent.name}")

        print("\n--- Testing with 'Translate 'Guten Tag' to German.' (Unsupported) ---")
        result_german = await Runner.run(
            triage_agent,
            "Translate 'Guten Tag' to German.",
            run_config=config,
            max_turns=5
        )
        print(f"Result (German - expected no handoff): {result_german.final_output}")
        print(f"Last Agent Name : {result.last_agent.name}")
        
        print("\n--- Testing with 'Tell me something interesting.' (Unclear) ---")
        result_unclear = await Runner.run(
            triage_agent,
            "Tell me something interesting.",
            run_config=config,
            max_turns=5
        )
        print(f"Result (Unclear - expected no handoff): {result_unclear.final_output}")
        print(f"Last Agent Name : {result.last_agent.name}")


    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

