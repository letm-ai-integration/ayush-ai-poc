from typing import Annotated, TypedDict, Optional
from operator import add


def merge_by_key(key: str):
    """Returns a reducer that concatenates lists of dicts, deduped by key."""

    def _reduce(existing: list[dict], new: list[dict]) -> list[dict]:
        combined = existing + new
        seen, unique = set(), []
        for item in combined:
            k = item.get(key)
            if k not in seen:
                seen.add(k)
                unique.append(item)
        return unique

    return _reduce


merge_flights = merge_by_key("airline")
merge_hotels = merge_by_key("name")


def merge_activities(existing: list[dict], new: list[dict]) -> list[dict]:
    return existing + new


class TripState(TypedDict):
    user_input: str
    preferences: Optional[dict]
    destination_options: list[dict]
    selected_destination: Optional[str]

    flight_options: Annotated[list[dict], merge_flights]
    hotel_options: Annotated[list[dict], merge_hotels]
    activities: Annotated[list[dict], merge_activities]
    weather_info: Optional[dict]

    budget_breakdown: Optional[dict]
    budget_approved: Optional[bool]

    final_itinerary: Optional[dict]

    iteration_count: int
    error_messages: Annotated[list[str], add]
    status: str
