from agents import Agent, Runner

async def get_agent_config():
    from agents import RunConfig, OpenAIChatCompletionsModel, set_tracing_disabled
    from openai import AsyncOpenAI
    from dotenv import load_dotenv
    import os

    load_dotenv()

    set_tracing_disabled(disabled=True)  # Disable OpenAI tracing

    API_KEY = os.getenv("API_KEY")
    BASE_URL = os.getenv("BASE_URL")
    MODEL_NAME = os.getenv("MODEL_NAME")

    if not API_KEY or not BASE_URL or not MODEL_NAME:
        raise ValueError("Please set the API_KEY, BASE_URL, and MODEL_NAME environment variables.")

    external_client = AsyncOpenAI(
        base_url=BASE_URL,
        api_key=API_KEY,
    )

    model= OpenAIChatCompletionsModel(
        openai_client=external_client,
        model=MODEL_NAME,
    )

    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True,
    )
    return config

agent= Agent(
    name="Assistant"
)

async def run_agent():
    result = await Runner.run(
        agent,
        "Hello",
        run_config=await get_agent_config(),
    )
    print(result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_agent())


# In Python, `asyncio.run()` is used to execute an asynchronous function from a synchronous context, such as the main entry point of a script.

# In your example, `run_agent()` is an asynchronous function that uses `await` to call `Runner.run()`, which is itself an async method. Since the top-level script (`if __name__ == "__main__":`) is synchronous, you cannot directly use `await` there.

# `asyncio.run(run_agent())` creates and manages an event loop, runs the async function until it completes, and then closes the event loop. This allows you to run async code in a standard Python script without needing to manually manage the event loop.

# **Without `asyncio.run()`, you would not be able to execute `await run_agent()` directly in the main block, because `await` can only be used inside async functions.**

# **In summary:**  
# - `asyncio.run()` bridges the gap between synchronous script entry points and asynchronous code, enabling you to run async agent logic in a standard Python script.

# This is a common and recommended pattern in Python async programming when you want to run async code from a synchronous context.

