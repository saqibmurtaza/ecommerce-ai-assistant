# OpenRouter Configuration for Agent SDK
# Modular Approach

def agent_config():
    """
    This function sets up the agent configuration for OpenRouter.
    It loads environment variables and initializes the OpenAI client.
    """
    from agents import (OpenAIChatCompletionsModel, set_tracing_disabled)
    from openai import AsyncOpenAI # chat completions
    from dotenv import load_dotenv
    import asyncio, os

    load_dotenv()

    set_tracing_disabled(disabled=True) # Open AI Tracing == Disable

    # OPENROUTER
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    BASE_URL = os.getenv("OPENROUTER_BASE_URL")
    MODEL_NAME = os.getenv("OPENROUTER_MODEL_GEMINI")

    if not OPENROUTER_API_KEY or not BASE_URL or not MODEL_NAME:
        raise ValueError("Please set OPENROUTER_API_KEY, OPENROUTER_BASE_URL, and MODEL_NAME in your environment variables.")

    external_client = AsyncOpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url=BASE_URL
    )

    model=OpenAIChatCompletionsModel(
        model=MODEL_NAME, 
        openai_client=external_client
        )
    
    return model
