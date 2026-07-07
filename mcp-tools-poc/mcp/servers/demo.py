import datetime
import random
from typing import Dict, Callable


class DemoMCP:
    """A demo MCP server with mock tools for demos."""

    name = "Demo MCP"

    FACTS = [
        "Our company was founded in 2010.",
        "We use a microservice architecture.",
        "Our shortest PR merged was 2 minutes.",
    ]

    def get_tools(self) -> Dict[str, Callable]:
        return {
            "company_information": self.company_information,
            "current_time": self.current_time,
            "random_fact": self.random_fact,
        }

    def company_information(self) -> str:
        return "We are a demo company that builds AI prototypes."

    def current_time(self) -> str:
        return datetime.datetime.now().isoformat()

    def random_fact(self) -> str:
        return random.choice(self.FACTS)
