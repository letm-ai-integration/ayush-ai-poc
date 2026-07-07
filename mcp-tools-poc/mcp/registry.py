from typing import List, Dict, Callable
from langchain_core.tools import tool

from .servers.local_system import LocalSystemMCP
from .servers.demo import DemoMCP
from logging_util import log_mcp_tool


def load_mcp_servers() -> List[object]:
    """Instantiate available MCP servers."""
    return [LocalSystemMCP(), DemoMCP()]


def get_wrapped_tools():
    """Return a list of langchain-compatible tool wrappers for all MCP tools."""
    servers = load_mcp_servers()
    wrapped = []

    for srv in servers:
        srv_name = getattr(srv, "name", srv.__class__.__name__)
        for tool_name, func in srv.get_tools().items():
            # Create a wrapper that invokes the MCP function via closure
            def make_wrapper(srv_name: str, tool_name: str, func: Callable):
                @tool(name_or_callable=tool_name, description=f"MCP tool {tool_name} from {srv_name}")
                def wrapper(*args, **kwargs):
                    # Log the MCP tool call
                    log_mcp_tool(srv_name, tool_name, args or kwargs or None)
                    return func(*args, **kwargs)

                return wrapper

            wrapped.append(make_wrapper(srv_name, tool_name, func))

    return wrapped
