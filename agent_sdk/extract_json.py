import json, asyncio
from typing_extensions import TypedDict, Any
from agents import Agent, FunctionTool, RunContextWrapper, function_tool, RunResult, ToolCallOutputItem
from agent_sdk.agent_config_module import get_agent_config

# Your provided extract_json_payload function
async def extract_json_payload(run_result: RunResult) -> str:
    # Scan the agent’s outputs in reverse order until we find a 
    # JSON-like message from a tool call.
    for item in reversed(run_result.new_items):
        if isinstance(item, ToolCallOutputItem) and item.output.strip().startswith("{"):
            return item.output.strip()
    # Fallback to an empty JSON object if nothing was found
    return "{}"

async def main():
    spanish_agent = Agent(
        name="Spanish agent",
        instructions="You translate the user's message to Spanish",
    )

    french_agent = Agent(
        name="French agent",
        instructions="You translate the user's message to French",
    )

    # Define a data_agent that will produce JSON output
    # For demonstration, let's make it return a hardcoded JSON string.
    # In a real scenario, this agent would perform some task to generate JSON.
    data_agent = Agent(
        name="Data Agent",
        instructions="You generate a JSON payload based on the user's request. Always respond with a valid JSON.",
    )

    # Create the json_tool using the data_agent and custom_output_extractor
    json_tool = data_agent.as_tool(
        tool_name="get_data_json",
        tool_description="Run the data agent and return only its JSON payload. Use this tool to get structured data.",
        custom_output_extractor=extract_json_payload,
    )

    orchestrator_agent = Agent(
        name="orchestrator_agent",
        instructions=(
            "You are a translation and data retrieval agent. You use the tools given to you to translate or retrieve data."
            "If asked for multiple translations, you call the relevant tools."
            "If asked for structured data, use the 'get_data_json' tool."
        ),
        tools=[
            spanish_agent.as_tool(
                tool_name="spanish_agent",
                tool_description="Translate the user's message to Spanish",
            ),
            french_agent.as_tool(
                tool_name="translate_to_french",
                tool_description="Translate the user's message to French",
            ),
            json_tool, # Add the json_tool here
        ],
    )

    from agents import Runner
    
    # Example 1: Using the translation agent (original functionality)
    print("--- Translation Example ---")
    result_translation = await Runner.run(
        orchestrator_agent, 
        input="Say 'Hello, how are you?' in Spanish.",
        run_config=await get_agent_config()
    )
    print(f"Translation result: {result_translation.final_output}")
    print("\n")

    # Example 2: Using the data agent to get JSON output
    print("--- Data Extraction Example ---")
    # To make the data_agent produce JSON, we'll need to guide it with the input.
    # In a real application, the data_agent's internal logic would handle JSON generation.
    # For this example, let's assume the data_agent is instructed to return a specific JSON.
    # You would typically have a more complex instruction for the data_agent itself if it's dynamic.
    # Here, we'll make the orchestrator ask the data_agent for "user info" which the data_agent is
    # pre-configured to respond with JSON.
    
    # To properly demonstrate, we need to ensure the `data_agent` itself returns JSON.
    # Let's modify the `data_agent` to always return a specific JSON for this demo.
    data_agent.instructions = "You are a data provider. When asked for user information, provide it in JSON format like: {'name': 'John Doe', 'age': 30, 'city': 'New York'}. Always ensure your output is valid JSON."

    result_json = await Runner.run(
        orchestrator_agent, 
        input="Get me user information as JSON.",
        run_config=await get_agent_config()
    )
    print(f"JSON result (raw): {result_json.final_output}")
    
    # If the `custom_output_extractor` worked, `final_output` should be the JSON string
    try:
        parsed_json = json.loads(result_json.final_output)
        print(f"JSON result (parsed): {json.dumps(parsed_json, indent=2)}")
    except json.JSONDecodeError:
        print("Final output was not valid JSON.")

if __name__ == "__main__":
    asyncio.run(main())