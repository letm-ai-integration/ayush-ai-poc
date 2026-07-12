import requests
from langsmith import traceable

from config import settings
from mock_data import FLIGHTS, HOTELS, ACTIVITIES, WEATHER


def _llm_query(prompt: str) -> str:
    """Thin LLM call — returns raw text. Agents own JSON parsing."""
    from langchain_groq import ChatGroq
    _llm = ChatGroq(api_key=settings.groq_api_key, model=settings.model_name, temperature=0.3)
    return _llm.invoke(prompt).content.strip()


@traceable(name="weather_lookup")
def weather_lookup(destination: str) -> dict:
    """
    Primary: OpenWeatherMap real-time data (if key present).
    Secondary: LLM seasonal knowledge.
    Emergency fallback: mock_data.
    """
    if settings.openweathermap_api_key:
        try:
            resp = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"q": destination, "appid": settings.openweathermap_api_key, "units": "metric"},
                timeout=8,
            )
            resp.raise_for_status()
            data = resp.json()
            print(f"  [Weather] Live data from OpenWeatherMap for {destination}")
            return {
                "avg_temp_celsius": round(data["main"]["temp"], 1),
                "feels_like_celsius": round(data["main"]["feels_like"], 1),
                "conditions": data["weather"][0]["description"],
                "humidity_pct": data["main"]["humidity"],
                "wind_speed_mps": data["wind"]["speed"],
                "warnings": [],
            }
        except Exception as e:
            print(f"  [Weather] OpenWeatherMap failed ({e}) — falling back to LLM knowledge")

    # LLM knowledge — returns raw text, agent will parse
    print(f"  [Weather] Using LLM knowledge for {destination}")
    return {"_llm_needed": True, "destination": destination}


@traceable(name="flight_search")
def flight_search(destination: str, origin: str = "Delhi", group_size: int = 1,
                  travel_style: str = "mid-range", budget_usd: int = 2000) -> list[dict]:
    """LLM knowledge for flights. mock_data used only as emergency fallback."""
    print(f"  [Flights] Using LLM knowledge for {origin} → {destination}")
    return {"_llm_needed": True, "destination": destination, "origin": origin,
            "group_size": group_size, "travel_style": travel_style, "budget_usd": budget_usd}


@traceable(name="hotel_search")
def hotel_search(destination: str, travel_style: str = "mid-range",
                 budget_usd: int = 2000, duration_days: int = 5, group_size: int = 1) -> list[dict]:
    """LLM knowledge for hotels. mock_data used only as emergency fallback."""
    print(f"  [Hotels] Using LLM knowledge for {destination}")
    return {"_llm_needed": True, "destination": destination, "travel_style": travel_style,
            "budget_usd": budget_usd, "duration_days": duration_days, "group_size": group_size}


@traceable(name="activity_search")
def activity_search(destination: str, interests: list = None,
                    travel_style: str = "mid-range", duration_days: int = 5) -> list[dict]:
    """LLM knowledge for activities. mock_data used only as emergency fallback."""
    print(f"  [Activities] Using LLM knowledge for {destination}")
    return {"_llm_needed": True, "destination": destination,
            "interests": interests or [], "travel_style": travel_style, "duration_days": duration_days}


def emergency_fallback_flights(destination: str) -> list[dict]:
    return FLIGHTS.get(destination, [{"airline": "Unknown", "departure_city": "Delhi",
                                       "arrival_city": destination, "price_usd": 800,
                                       "duration_hours": 10.0, "stops": 1, "class_type": "economy"}])


def emergency_fallback_hotels(destination: str) -> list[dict]:
    return HOTELS.get(destination, [{"name": f"{destination} Hotel", "price_per_night_usd": 100,
                                      "rating": 4.0, "style": "mid-range", "neighborhood": "City Center"}])


def emergency_fallback_activities(destination: str) -> list[dict]:
    return ACTIVITIES.get(destination, [{"name": f"Explore {destination}", "category": "sightseeing",
                                          "cost_usd": 0, "time_of_day": "morning", "day_number": 1}])


def emergency_fallback_weather(destination: str) -> dict:
    return WEATHER.get(destination, {"avg_temp_celsius": 20, "conditions": "pleasant",
                                      "warnings": [], "packing_suggestions": [], "cultural_tips": []})
