import json
import re

from langchain_groq import ChatGroq
from langsmith import traceable

import prompts
from config import settings
from search_tools import search_destination, search_travel_info
from state import TripState
from tools import (
    flight_search, hotel_search, activity_search, weather_lookup,
    emergency_fallback_flights, emergency_fallback_hotels,
    emergency_fallback_activities, emergency_fallback_weather,
)

llm = ChatGroq(api_key=settings.groq_api_key, model=settings.model_name, temperature=0.3)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _clean_json(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"```$", "", text)
    return text.strip()


@traceable(name="llm_json")
def _llm_json(prompt: str) -> dict | list:
    for attempt in range(2):
        try:
            resp = llm.invoke(prompt)
            return json.loads(_clean_json(resp.content))
        except Exception as e:
            print(f"  [LLM] JSON parse failed (attempt {attempt + 1}): {e}")
    return {}


def run_json_prompt(prompt_template: str, **kwargs) -> dict | list:
    return _llm_json(prompt_template.format(**kwargs))


# ---------------------------------------------------------------------------
# Fallbacks
# ---------------------------------------------------------------------------

def fallback_preferences() -> dict:
    return {"destination_hints": [], "budget_usd": 2000, "duration_days": 5,
            "interests": ["sightseeing"], "dietary_restrictions": [],
            "travel_style": "mid-range", "group_size": 1}


def fallback_destinations() -> list:
    return [
        {"name": "Tokyo", "country": "Japan", "reason": "Rich culture and food scene", "estimated_daily_cost_usd": 120, "match_score": 0.9},
        {"name": "Bali", "country": "Indonesia", "reason": "Affordable tropical escape", "estimated_daily_cost_usd": 95, "match_score": 0.85},
        {"name": "Barcelona", "country": "Spain", "reason": "Art, architecture and beaches", "estimated_daily_cost_usd": 110, "match_score": 0.8},
    ]


def fallback_weather() -> dict:
    return {"avg_temp_celsius": 20, "conditions": "pleasant", "warnings": [],
            "packing_suggestions": ["Light layers"], "cultural_tips": ["Respect local customs"]}


def fallback_budget() -> dict:
    return {"flights_total": 800, "accommodation_total": 500, "activities_total": 100,
            "food_estimate": 200, "transport_estimate": 50, "total_estimated": 1650,
            "is_over_budget": False, "savings_suggestions": []}


def fallback_itinerary() -> dict:
    return {"title": "Trip", "destination": "Unknown", "dates": "TBD",
            "days": [{"day_number": 1, "theme": "Arrival", "activities": [], "estimated_cost": 0}],
            "budget_summary": {}, "packing_list": [], "important_tips": []}


# ---------------------------------------------------------------------------
# Nodes
# ---------------------------------------------------------------------------

@traceable(name="preference_parser")
def preference_parser_node(state: TripState) -> dict:
    print("[Preference Parser] Extracting preferences...")
    result = run_json_prompt(prompts.PREFERENCE_PARSER_PROMPT, user_input=state["user_input"])
    return {"preferences": result or fallback_preferences(), "status": "parsing"}


@traceable(name="destination_researcher")
def destination_researcher_node(state: TripState) -> dict:
    print("[Research Agent] Searching DuckDuckGo...")
    prefs = state.get("preferences") or {}
    hints = prefs.get("destination_hints", [])
    interests = prefs.get("interests", [])
    budget = prefs.get("budget_usd", 2000)
    style = prefs.get("travel_style", "mid-range")

    hint_str = f"specifically {', '.join(hints)}" if hints else ""
    query = f"Best travel destinations {hint_str} for {', '.join(interests) or 'sightseeing'} with a budget of {budget} USD {style} traveler"
    search_results = search_destination(query) + "\n\n" + search_travel_info(", ".join(hints) if hints else "popular travel destinations")

    print("[Research Agent] LLM reasoning over search results...")
    result = run_json_prompt(prompts.RESEARCH_AGENT_PROMPT, preferences=prefs, search_results=search_results)
    options = result if isinstance(result, list) and result else fallback_destinations()
    return {"destination_options": options, "status": "awaiting_destination_choice"}


@traceable(name="flight_finder")
def flight_finder_node(state: TripState) -> dict:
    prefs = state.get("preferences") or {}
    style = prefs.get("travel_style", "mid-range")
    budget = prefs.get("budget_usd", 2000)
    group_size = prefs.get("group_size", 1)
    destination = state["selected_destination"]

    signal = flight_search(destination, group_size=group_size, travel_style=style, budget_usd=budget)

    print(f"[Flight Agent] Generating flights to {destination} using LLM knowledge...")
    raw = run_json_prompt(
        prompts.FLIGHT_KNOWLEDGE_PROMPT,
        destination=destination,
        origin=signal.get("origin", "Delhi"),
        group_size=group_size,
        travel_style=style,
        budget_usd=budget,
    )
    if not isinstance(raw, list) or not raw:
        print("  [Flight Agent] LLM generation failed — using emergency fallback")
        raw = emergency_fallback_flights(destination)

    print(f"[Flight Agent] Ranking {len(raw)} flights...")
    ranked = run_json_prompt(prompts.FLIGHT_RANKER_PROMPT, flights=raw, travel_style=style)
    return {"flight_options": ranked if isinstance(ranked, list) else raw}


@traceable(name="accommodation_scout")
def accommodation_scout_node(state: TripState) -> dict:
    prefs = state.get("preferences") or {}
    style = prefs.get("travel_style", "mid-range")
    budget = prefs.get("budget_usd", 2000)
    duration = prefs.get("duration_days", 5)
    group_size = prefs.get("group_size", 1)
    destination = state["selected_destination"]

    hotel_search(destination, travel_style=style, budget_usd=budget, duration_days=duration, group_size=group_size)

    print(f"[Hotel Agent] Generating hotels in {destination} using LLM knowledge...")
    raw = run_json_prompt(
        prompts.HOTEL_KNOWLEDGE_PROMPT,
        destination=destination,
        travel_style=style,
        budget_usd=budget,
        duration_days=duration,
        group_size=group_size,
    )
    if not isinstance(raw, list) or not raw:
        print("  [Hotel Agent] LLM generation failed — using emergency fallback")
        raw = emergency_fallback_hotels(destination)

    print(f"[Hotel Agent] Ranking {len(raw)} hotels...")
    ranked = run_json_prompt(prompts.HOTEL_RANKER_PROMPT, hotels=raw, travel_style=style, budget_usd=budget)
    return {"hotel_options": ranked if isinstance(ranked, list) else raw}


@traceable(name="activity_planner")
def activity_planner_node(state: TripState) -> dict:
    prefs = state.get("preferences") or {}
    interests = prefs.get("interests", [])
    style = prefs.get("travel_style", "mid-range")
    duration = prefs.get("duration_days", 5)
    destination = state["selected_destination"]

    activity_search(destination, interests=interests, travel_style=style, duration_days=duration)

    print(f"[Activity Agent] Generating activities for {destination} using LLM knowledge...")
    raw = run_json_prompt(
        prompts.ACTIVITY_KNOWLEDGE_PROMPT,
        destination=destination,
        interests=", ".join(interests) or "general sightseeing",
        travel_style=style,
        duration_days=duration,
    )
    if not isinstance(raw, list) or not raw:
        print("  [Activity Agent] LLM generation failed — using emergency fallback")
        raw = emergency_fallback_activities(destination)

    print(f"[Activity Agent] Planning {len(raw)} activities across {duration} days...")
    planned = run_json_prompt(prompts.ACTIVITY_PLANNER_PROMPT, preferences=prefs, raw_activities=raw, duration_days=duration)
    return {"activities": planned if isinstance(planned, list) else raw}


@traceable(name="weather_advisor")
def weather_advisor_node(state: TripState) -> dict:
    destination = state["selected_destination"]
    print(f"[Weather Agent] Getting weather for {destination}...")

    signal = weather_lookup(destination)

    if signal.get("_llm_needed"):
        enriched = run_json_prompt(prompts.WEATHER_KNOWLEDGE_PROMPT, destination=destination)
        if not isinstance(enriched, dict) or not enriched:
            print("  [Weather Agent] LLM generation failed — using emergency fallback")
            enriched = emergency_fallback_weather(destination)
    else:
        # Real data from OpenWeatherMap — ask LLM to add packing/cultural tips
        enriched = run_json_prompt(
            """Given this real weather data: {weather} for {destination},
add "packing_suggestions" (list) and "cultural_tips" (list) and return the full dict as ONLY JSON.""",
            weather=signal, destination=destination,
        )
        if not isinstance(enriched, dict) or not enriched:
            enriched = signal

    return {"weather_info": enriched}


@traceable(name="budget_calculator")
def budget_calculator_node(state: TripState) -> dict:
    prefs = state.get("preferences") or {}
    print("[Budget Agent] Calculating trip cost...")
    breakdown = run_json_prompt(
        prompts.BUDGET_CALCULATOR_PROMPT,
        flights=state.get("flight_options", []),
        hotels=state.get("hotel_options", []),
        activities=state.get("activities", []),
        nights=prefs.get("duration_days", 5),
        budget_usd=prefs.get("budget_usd", 2000),
        group_size=prefs.get("group_size", 1),
    )
    return {"budget_breakdown": breakdown if isinstance(breakdown, dict) else fallback_budget(), "status": "budgeting"}


@traceable(name="itinerary_compiler")
def itinerary_compiler_node(state: TripState) -> dict:
    print("[Itinerary Agent] Compiling final itinerary...")
    final = run_json_prompt(
        prompts.ITINERARY_COMPILER_PROMPT,
        destination=state["selected_destination"],
        preferences=state.get("preferences", {}),
        activities=state.get("activities", []),
        weather=state.get("weather_info", {}),
        budget_breakdown=state.get("budget_breakdown", {}),
    )
    return {"final_itinerary": final if isinstance(final, dict) else fallback_itinerary(), "status": "done"}


def human_select_destination_node(state: TripState) -> dict:
    return {}


def human_approve_budget_node(state: TripState) -> dict:
    return {}
