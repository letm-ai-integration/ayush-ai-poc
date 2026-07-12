from langchain_community.tools import DuckDuckGoSearchRun
from langsmith import traceable

search = DuckDuckGoSearchRun()


def _run(query: str) -> str:
    try:
        result = search.run(query)
        return result.strip() if result else "No results found."
    except Exception as e:
        return f"Search failed: {e}"


@traceable(name="search_destination")
def search_destination(query: str) -> str:
    return _run(f"Best travel destinations: {query}")


@traceable(name="search_weather")
def search_weather(destination: str) -> str:
    return _run(f"Weather and climate in {destination} for tourists best time to visit")


@traceable(name="search_events")
def search_events(destination: str) -> str:
    return _run(f"Top events festivals and things to do in {destination}")


@traceable(name="search_travel_info")
def search_travel_info(destination: str) -> str:
    return _run(f"Travel guide tips budget cost of living for tourists in {destination}")
