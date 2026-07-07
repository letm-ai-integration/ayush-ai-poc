import platform
import socket
from typing import Dict, Callable


class LocalSystemMCP:
    """A tiny MCP server exposing deterministic system info tools."""

    name = "Local System MCP"

    def get_tools(self) -> Dict[str, Callable]:
        return {
            "get_hostname": self.get_hostname,
            "get_os_name": self.get_os_name,
            "current_directory": self.current_directory,
            "python_version": self.python_version,
        }

    def get_hostname(self) -> str:
        return socket.gethostname()

    def get_os_name(self) -> str:
        return platform.system()

    def current_directory(self) -> str:
        import os

        return os.getcwd()

    def python_version(self) -> str:
        import sys

        return sys.version
