import os

from dotenv import load_dotenv

from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from core.enums import AgentType
from prompts.definitions import HR_PROMPT, PROJECT_PROMPT
from tools import analyze_project, lookup_company_policy, write_file

from mcp.registry import get_wrapped_tools
from logging_util import get_last_execution, log_llm_response, clear_last_execution

load_dotenv()

llm = ChatGroq(
    model=os.getenv("MODEL_NAME"),
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
)

def build_agent_registry():
    hr_agent = create_react_agent(
        model=llm,
        tools=[lookup_company_policy],
        prompt=HR_PROMPT,
    )

    developer_agent = create_react_agent(
        model=llm,
        tools=[
            analyze_project,
            write_file,
        ],
        prompt=PROJECT_PROMPT,
    )

    # Discover MCP tools and append to each agent's tool list
    mcp_tools = get_wrapped_tools()

    # Rebuild agents with combined tool lists to include MCP tools
    hr_agent = create_react_agent(
        model=llm,
        tools=[lookup_company_policy] + mcp_tools,
        prompt=HR_PROMPT,
    )

    developer_agent = create_react_agent(
        model=llm,
        tools=[analyze_project, write_file] + mcp_tools,
        prompt=PROJECT_PROMPT,
    )

    return {
        AgentType.HR: hr_agent,
        AgentType.DEVELOPER: developer_agent,
    }


AGENTS = build_agent_registry()


# -------------------------
# Chat
# -------------------------

def chat(user_message: str, mode: str) -> str:

    print(f"\n👤 User: {user_message}")
    print(f"🤖 Agent: {mode}")

    agent = AGENTS.get(mode)

    if agent is None:
        raise ValueError(f"Unknown mode: {mode}")

    # Only the Developer Agent needs the project path.
    if mode == "Developer Agent":
        # project_path would be passed in the user_message for the Developer Agent
        pass

    response = agent.invoke(
        {
            "messages": [
                HumanMessage(content=user_message)
            ]
        }
    )

    messages = response["messages"]

    final_answer = messages[-1].content

    # Retrieve last execution metadata from the centralized logger
    meta = get_last_execution()

    if not meta:
        # No tool was invoked
        log_llm_response()
        meta = get_last_execution()

    # Append execution metadata to the LLM response so the UI can display it
    meta_block = (
        "\n\n---\nExecution Info:\n"
        f"Current Agent: {mode}\n"
        f"Tool Category: {meta.get('category')}\n"
        f"Tool Name: {meta.get('tool_name')}\n"
        f"Server: {meta.get('server')}\n"
    )

    # Clear last execution for next call
    clear_last_execution()

    print(f"\n🤖 Response:\n{final_answer}\n")

    return final_answer + meta_block