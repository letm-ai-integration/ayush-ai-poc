from typing import Any, Dict, List, Callable


class MCPClient:
    """A minimal MCP client for discovering and invoking server tools."""

    def __init__(self, servers: List[Any]):
        # servers are instances with .name and .get_tools()
        self._servers = {s.name: s for s in servers}

    def list_servers(self) -> List[str]:
        return list(self._servers.keys())

    def list_tools(self, server_name: str) -> List[str]:
        srv = self._servers.get(server_name)
        if not srv:
            return []
        return list(srv.get_tools().keys())

    def invoke(self, server_name: str, tool_name: str, *args, **kwargs) -> Any:
        srv = self._servers.get(server_name)
        if not srv:
            raise ValueError(f"Unknown MCP server: {server_name}")
        tools = srv.get_tools()
        func = tools.get(tool_name)
        if not func:
            raise ValueError(f"Unknown tool '{tool_name}' on server '{server_name}'")
        return func(*args, **kwargs)
