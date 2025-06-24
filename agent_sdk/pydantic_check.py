# # ##########################################
# # # Example: Tool Output Validation with Pydantic

# from pydantic import BaseModel
# from agents import tool, Agent, Runner, function_tool
# from agent_sdk.agent_config_module import get_agent_config

# # Define the output schema using Pydantic
# class AddResult(BaseModel):
#     sum: int

# class AgentOutput(BaseModel):
#     message: int
#     calculated_sum: int

# # Define the tool with type annotations and output schema
# @function_tool
# def add_numbers(a: int, b: int) -> str: # Tool returns a string
#     actual_sum = a + b
#     print(f"Tool executed. Sum: {actual_sum}")
#     # return f"The calculation result is {actual_sum}." # Simple string output
#     return '{"msg": "error", "calculated_sum": "eight"}'  # wrong keys and types

# # Create an agent that uses this tool
# from agents.agent_output import AgentOutputSchema
# agent = Agent(
#     name="Adder",
#     instructions="Add two numbers and return the result as a JSON object.",
#     tools=[add_numbers],
#     output_type=AgentOutputSchema(
#         output_type=AgentOutput,
#         strict_json_schema=True,  # Enable strict JSON schema validation
#     )
# )

# # Run the agent
# async def run_agent():
#     result = await Runner.run(agent, 
#                             "Add 3 and 5", 
#                             run_config=await get_agent_config()
#     )

#     print(f"result: {result}")        # Output: AddResult(sum=8)
#     # print(f"final_output: {result.final_output}")    # Output: 8
    

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(run_agent())

# ######################################################

from pydantic import BaseModel
from agents import tool, Agent, Runner, function_tool
from agent_sdk.agent_config_module import get_agent_config
from agents.agent_output import AgentOutputSchema
import json

# Define output schemas
class AddResult(BaseModel):
    sum: int

class AgentOutput(BaseModel):
    message: str
    calculated_sum: int

# Define a tool that returns a string
@function_tool
def add_numbers(a: int, b: int) -> str:
    actual_sum = a + b
    print(f"Tool executed. Sum: {actual_sum}")
    return f"The calculation result is {actual_sum}."


# Create the agent
agent = Agent(
    name="Adder",
    instructions="Add two numbers and return the result as a JSON object.",
    tools=[add_numbers],
)

# Agent output schema instance
agent_output_schema = AgentOutputSchema(AgentOutput)

# Run the agent
async def run_agent():
    result = await Runner.run(
        agent, 
        "Add 3 and 5", 
        run_config=await get_agent_config()
    )

    print(f"\nRaw result: {result}")

    # Validate using schema
    if isinstance(result.final_output, str):
        try:
            validated = agent_output_schema.validate_json(result.final_output)
            print(f"\n✅ Validated Output as AgentOutput: {validated}")
        except Exception as e:
            print(f"\n❌ Validation failed: {e}")
    else:
        print("⏭ Skipped: final_output is not a string, so no validation done.")
    
    print(f"\nSchema: {agent_output_schema.json_schema()}")
    print(f"Strict mode? {agent_output_schema.is_strict_json_schema()}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_agent())
