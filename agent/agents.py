# /agent/agents.py

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent

# import the prompts and tools
from prompts import SYSTEM_PROMPT
from tools import (
    list_active_alerts,
    query_prometheus,
    consult_runbook,
    generate_dry_run_plan
)

# Loading environment variables (reading .env)
load_dotenv()

# Initialize the large language model (compatible with Qwen/DashScope)
llm = ChatOpenAI(
    model=os.getenv("CUSTOM_MODEL_NAME", "qwen-plus"),
    api_key=os.getenv("CUSTOM_MODEL_API_KEY"),
    base_url=os.getenv("CUSTOM_MODEL_BASE_URL"),
    temperature=0
)

# Prepare Tools
tools = [
    list_active_alerts,
    query_prometheus,
    consult_runbook,
    generate_dry_run_plan
]

# Creating an Agent (ReAct mode)
# This is a pre-built Agent that automatically understands the cycle of: "Think -> Find a tool -> Observe the result -> Think again"
agent_runnable = create_react_agent(
    model=llm,
    tools=tools,
    state_modifier=SYSTEM_PROMPT # Instilling the SRE mindset
)

# Helper function, used by graph.py
def get_agent():
    return agent_runnable