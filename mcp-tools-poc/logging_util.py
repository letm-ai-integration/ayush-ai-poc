from typing import Any, Dict, Optional
import threading

_last_execution: Dict[str, Any] = {}
_lock = threading.Lock()


def _print_block(lines: str) -> None:
    print("\n" + "#" * 40)
    print(lines)
    print("#" * 40 + "\n")


def log_local_tool(tool_name: str, args: Optional[Any] = None) -> None:
    args_display = args if args else "None"
    lines = (
        "LOCAL TOOL\n"
        f"Tool:\n{tool_name}\n\n"
        f"Arguments:\n{args_display}\n"
    )
    _print_block(lines)
    with _lock:
        _last_execution.clear()
        _last_execution.update({
            "category": "Local Tool",
            "tool_name": tool_name,
            "server": None,
            "args": args,
        })


def log_mcp_tool(server: str, tool_name: str, args: Optional[Any] = None) -> None:
    args_display = args if args else "None"
    lines = (
        "MCP TOOL\n"
        f"Server:\n{server}\n\n"
        f"Tool:\n{tool_name}\n\n"
        f"Arguments:\n{args_display}\n"
    )
    _print_block(lines)
    with _lock:
        _last_execution.clear()
        _last_execution.update({
            "category": "MCP Tool",
            "tool_name": tool_name,
            "server": server,
            "args": args,
        })


def log_llm_response() -> None:
    lines = "LLM RESPONSE\nNo Tool Invoked\n"
    _print_block(lines)
    with _lock:
        _last_execution.clear()
        _last_execution.update({
            "category": "No Tool",
            "tool_name": None,
            "server": None,
            "args": None,
        })


def get_last_execution() -> Dict[str, Any]:
    with _lock:
        return dict(_last_execution)


def clear_last_execution() -> None:
    with _lock:
        _last_execution.clear()
