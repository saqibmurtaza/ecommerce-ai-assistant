from agents import Agent, RunConfig, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, set_default_openai_api
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

##########################
# AGENT CONFIG
#########################
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

#######################
# DYNAMIC INSRUCTIONS
#######################

from pydantic import BaseModel
# Define the context
class UserContext(BaseModel):
    name: str
    preferred_category: str
    is_vip: bool = False


# 🛒 Example: Dynamic Instructions for a Personalized Shopping Assistant
# you can also provide dynamic instructions via a function. The function will receive the agent and context, and must return the prompt. Both regular and async functions are accepted.
from agents import RunContextWrapper

def dynamic_instructions(
        ctx: RunContextWrapper[UserContext], 
        agent: Agent[UserContext]) -> str:
    
    vip_note = "As a VIP customer, you may get early access to exclusive deals."if ctx.context.is_vip else ""
  
    return (
        f"You are a shopping assistant for {ctx.context.name}. "
        f"They are browsing in the '{ctx.context.preferred_category}' category. "
        f"Help them find trending products and give smart recommendations. "
        f"If a discount is available, mention it."
        f" {vip_note} "
    )

# DEFINE AGENT
shopping_agent= Agent(
    name= "ShoppingAssistant",
    instructions= dynamic_instructions,
 )

# INITIATE CONTEXT
user_context = UserContext(
    name="Saqib",
    preferred_category="Shoes",
    is_vip=True
)

import uuid
print("🆔 Run ID:", uuid.uuid4())
# RUNNER
dynamic_result= Runner.run_sync(
    shopping_agent,
    "What are the best-selling SHOES this week?",
    context=user_context,
    run_config=config
)
print(dynamic_result.final_output)

#############
#AGENT HOOKS\
#################

# A class that receives callbacks on various lifecycle events for a specific agent. 
# You can set this on agent.hooks to receive events for that specific agent.
# agent.hooks = MyHookClass()	Attach a whole class of lifecycle callbacks at once

from agents import AgentHooks
from typing import Any

class ShoppingHooks(AgentHooks[UserContext]):
    async def on_start(
            self,
            ctx: RunContextWrapper[UserContext],
            agent: Agent[UserContext]
        ) -> None:
        print(f"[START] {ctx.context.name} started shopping in {ctx.context.preferred_category} category.")
        print(f"Agent {agent.name}")

    async def on_end(
            self,
            ctx: RunContextWrapper[UserContext],
            agent: Agent[UserContext],
            output: Any
    ) -> None:
    
        print("🟡 [HOOK] on_end triggered")
        print(f"🧑 User: {ctx.context.name}")
        print(f"🎯 Preferred Category: {ctx.context.preferred_category}")
        print(f"👑 VIP Status: {ctx.context.is_vip}")
        print(f"🤖 Agent: {agent.name}")
        print(f"🧰 Tools: {[tool.name for tool in agent.tools] if agent.tools else 'No tools loaded'}")
        print(f"📝 Final Output:{output}")

    async def on_handoff(
            self, 
            ctx: RunContextWrapper[UserContext], 
            agent: Agent[UserContext], 
            source: Agent[UserContext]
            ) -> None:
            print("🔁 [HANDOFF] Agent Handoff Detected!")
            print(f"👤 User: {ctx.context.name}")
            print(f"📦 From Agent: {source.name}")
            print(f"➡️ To Agent: {agent.name}")
        
import uuid
print("🆔 Run ID:", uuid.uuid4())

hook_agent= shopping_agent.clone(
    name="HookedShoppingAssistant",
    instructions=dynamic_instructions,
)
########################################
#  ✅ Assign Hooks to Your Agent
hook_agent.hooks= ShoppingHooks()
###########################################
hook_result= Runner.run_sync(
    hook_agent,
    "What are the best-selling shoes this week?",
    context=user_context,
    run_config=config
)

discount_agent= Agent(
    name= "DiscountShoppingAssistant",
    instructions= "Handles VIP discount queries",
)


async def main():
    print("🆔 Run ID:", uuid.uuid4())

    # Optional handoff before execution
    # Manually trigger handoff for demo
    await hook_agent.hooks.on_handoff(
        RunContextWrapper(context=user_context),
        discount_agent,  # source
        hook_agent       # destination
    )

    discount_result = await Runner.run(
        discount_agent,
         "Are there any VIP discounts on these shoes?",
        context=user_context,
        run_config=config
    )
    print("\n✅ Final Discount Agent Output:\n", discount_result.final_output)

import asyncio
asyncio.run(main())

